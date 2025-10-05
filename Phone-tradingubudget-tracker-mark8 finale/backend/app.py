from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__, static_folder='../frontend', static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///phone_manager.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Fix CORS configuration
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5000", "http://127.0.0.1:5000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

db = SQLAlchemy(app)

# Models
class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_money = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Phone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    buy_price = db.Column(db.Float, nullable=False)
    sell_price = db.Column(db.Float, nullable=True)
    state = db.Column(db.String(20), default='bought')  # bought, sold, scammed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    notes = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'model': self.model,
            'brand': self.brand,
            'buy_price': self.buy_price,
            'sell_price': self.sell_price,
            'state': self.state,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'notes': self.notes,
            'profit': (self.sell_price - self.buy_price) if self.sell_price else None
        }

# Deal evaluation logic
def evaluate_deal(phone, action_type):
    messages = []
    
    if action_type == 'buy':
        # Example evaluation for buying
        if phone.buy_price < 200:
            messages.append({
                'type': 'success',
                'message': f'Great deal! {phone.brand} {phone.model} for ${phone.buy_price} is below market average.'
            })
        elif phone.buy_price > 800:
            messages.append({
                'type': 'warning',
                'message': f'High investment! Make sure you can sell this {phone.brand} {phone.model} for a good profit.'
            })
        else:
            messages.append({
                'type': 'info',
                'message': f'Fair price for {phone.brand} {phone.model}. Check market trends before buying.'
            })
    
    elif action_type == 'sell' and phone.sell_price:
        profit = phone.sell_price - phone.buy_price
        profit_percentage = (profit / phone.buy_price) * 100
        
        if profit_percentage > 30:
            messages.append({
                'type': 'success',
                'message': f'Excellent! You made ${profit:.2f} ({profit_percentage:.1f}%) profit on this {phone.brand} {phone.model}!'
            })
        elif profit_percentage > 10:
            messages.append({
                'type': 'success',
                'message': f'Good profit! You made ${profit:.2f} ({profit_percentage:.1f}%) on this sale.'
            })
        elif profit > 0:
            messages.append({
                'type': 'info',
                'message': f'Small profit of ${profit:.2f}. Consider if it was worth your time and effort.'
            })
        else:
            messages.append({
                'type': 'warning',
                'message': f'You lost ${abs(profit):.2f} on this sale. Review your buying strategy.'
            })
    
    elif action_type == 'scam':
        messages.append({
            'type': 'error',
            'message': f'Sorry for your loss! You lost ${phone.buy_price} to a scam. Be more careful with future transactions.'
        })
    
    return messages

# Routes
@app.route('/api/budget', methods=['GET'])
def get_budget():
    budget = Budget.query.first()
    if not budget:
        budget = Budget(total_money=0.0)
        db.session.add(budget)
        db.session.commit()
    
    return jsonify({
        'total_money': budget.total_money,
        'updated_at': budget.updated_at.isoformat()
    })

@app.route('/api/budget', methods=['POST'])
def update_budget():
    data = request.get_json()
    budget = Budget.query.first()
    
    if not budget:
        budget = Budget(total_money=data.get('total_money', 0.0))
        db.session.add(budget)
    else:
        budget.total_money = data.get('total_money', budget.total_money)
        budget.updated_at = datetime.utcnow()
    
    db.session.commit()
    return jsonify({
        'total_money': budget.total_money,
        'updated_at': budget.updated_at.isoformat()
    })

@app.route('/api/phones', methods=['GET'])
def get_phones():
    phones = Phone.query.order_by(Phone.created_at.desc()).all()
    return jsonify([phone.to_dict() for phone in phones])

@app.route('/api/phones', methods=['POST'])
def add_phone():
    data = request.get_json()
    
    phone = Phone(
        model=data['model'],
        brand=data['brand'],
        buy_price=float(data['buy_price']),
        notes=data.get('notes', '')
    )
    
    db.session.add(phone)
    
    # Update budget (subtract money spent)
    budget = Budget.query.first()
    if budget:
        budget.total_money -= phone.buy_price
        budget.updated_at = datetime.utcnow()
    
    db.session.commit()
    
    # Get deal evaluation
    messages = evaluate_deal(phone, 'buy')
    
    return jsonify({
        'phone': phone.to_dict(),
        'messages': messages
    })

@app.route('/api/phones/<int:phone_id>/state', methods=['PUT', 'OPTIONS'])
def update_phone_state(phone_id):
    # Handle CORS preflight request
    if request.method == 'OPTIONS':
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'PUT')
        return response
        
    data = request.get_json()
    
    phone = Phone.query.get_or_404(phone_id)
    old_state = phone.state
    new_state = data['state']
    
    budget = Budget.query.first()
    messages = []
    
    # Handle state transitions and budget updates
    if old_state == 'bought' and new_state == 'sold':
        sell_price = float(data['sell_price'])
        phone.sell_price = sell_price
        phone.state = new_state
        
        # Add money from sale to budget
        if budget:
            budget.total_money += sell_price
            budget.updated_at = datetime.utcnow()
        
        messages = evaluate_deal(phone, 'sell')
    
    elif old_state == 'bought' and new_state == 'scammed':
        phone.state = new_state
        # Money already deducted when bought, no need to deduct again
        messages = evaluate_deal(phone, 'scam')
    
    elif old_state == 'sold' and new_state == 'scammed':
        phone.state = new_state
        
        # Remove the money we got from selling (since it was a scam)
        if budget and phone.sell_price:
            budget.total_money -= phone.sell_price
            budget.updated_at = datetime.utcnow()
        
        messages = evaluate_deal(phone, 'scam')
    
    elif old_state == 'scammed' and new_state == 'sold':
        sell_price = float(data['sell_price'])
        phone.sell_price = sell_price
        phone.state = new_state
        
        # Add money from sale to budget
        if budget:
            budget.total_money += sell_price
            budget.updated_at = datetime.utcnow()
        
        messages = evaluate_deal(phone, 'sell')
    
    phone.updated_at = datetime.utcnow()
    db.session.commit()
    
    response = jsonify({
        'phone': phone.to_dict(),
        'messages': messages
    })
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    return response

@app.route('/api/phones/<int:phone_id>', methods=['DELETE', 'OPTIONS'])
def delete_phone(phone_id):
    # Handle CORS preflight request
    if request.method == 'OPTIONS':
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'DELETE')
        return response
        
    phone = Phone.query.get_or_404(phone_id)
    
    # Refund money if phone was just bought
    if phone.state == 'bought':
        budget = Budget.query.first()
        if budget:
            budget.total_money += phone.buy_price
            budget.updated_at = datetime.utcnow()
    
    db.session.delete(phone)
    db.session.commit()
    
    response = jsonify({'message': 'Phone deleted successfully'})
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    return response

# Serve frontend
@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

@app.route('/api/stats', methods=['GET'])
def get_stats():
    phones = Phone.query.all()
    
    total_bought = len([p for p in phones if p.state in ['bought', 'sold', 'scammed']])
    total_sold = len([p for p in phones if p.state == 'sold'])
    total_scammed = len([p for p in phones if p.state == 'scammed'])
    
    total_invested = sum(p.buy_price for p in phones)
    total_revenue = sum(p.sell_price for p in phones if p.sell_price)
    total_profit = total_revenue - sum(p.buy_price for p in phones if p.state == 'sold')
    total_lost = sum(p.buy_price for p in phones if p.state == 'scammed')
    
    return jsonify({
        'total_bought': total_bought,
        'total_sold': total_sold,
        'total_scammed': total_scammed,
        'total_invested': total_invested,
        'total_revenue': total_revenue,
        'total_profit': total_profit,
        'total_lost': total_lost
    })




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)