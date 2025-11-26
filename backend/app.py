from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from database import db
from models import Phone, Budget
import logic
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

def create_app(test_config=None):
    app = Flask(__name__, static_folder='../frontend', static_url_path='')

    # Metrics Setup 
    metrics = PrometheusMetrics(app, path=None) 
    
    metrics.info('app_info', 'Application info', version='1.0.0')

    # Configuration
    if test_config:
        app.config.update(test_config)
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///phone_manager.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize Plugins
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    db.init_app(app)

    # --- Routes ---

    @app.route('/metrics')
    def metrics_endpoint():
        return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

    # Health Check
    @app.route('/health')
    @metrics.do_not_track()
    def health_check():
        return jsonify({
            "status": "healthy",
            "uptime": "up",
            "db_connection": "active"
        }), 200

    @app.route('/api/budget', methods=['GET'])
    def get_budget():
        budget = logic.get_or_create_budget()
        return jsonify({
            'total_money': budget.total_money,
            'updated_at': budget.updated_at.isoformat()
        })

    @app.route('/api/budget', methods=['POST'])
    def update_budget():
        data = request.get_json()
        budget = logic.get_or_create_budget()
        budget.total_money = data.get('total_money', budget.total_money)
        db.session.commit()
        return jsonify({'total_money': budget.total_money})

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
        logic.update_budget_transaction(-phone.buy_price)
        db.session.commit()
        messages = logic.evaluate_deal(phone, 'buy')
        return jsonify({'phone': phone.to_dict(), 'messages': messages})

    @app.route('/api/phones/<int:phone_id>/state', methods=['PUT'])
    def update_phone_state(phone_id):
        data = request.get_json()
        phone = Phone.query.get_or_404(phone_id)
        messages = logic.handle_state_change(phone, data['state'], data.get('sell_price'))
        db.session.commit()
        return jsonify({'phone': phone.to_dict(), 'messages': messages})

    @app.route('/api/phones/<int:phone_id>', methods=['DELETE'])
    def delete_phone(phone_id):
        phone = Phone.query.get_or_404(phone_id)
        if phone.state == logic.STATE_BOUGHT:
            logic.update_budget_transaction(phone.buy_price)
        db.session.delete(phone)
        db.session.commit()
        return jsonify({'message': 'Phone deleted successfully'})

    @app.route('/api/stats', methods=['GET'])
    def get_stats():
        phones = Phone.query.all()
        bought = [p for p in phones if p.state in [logic.STATE_BOUGHT, logic.STATE_SOLD, logic.STATE_SCAMMED]]
        sold = [p for p in phones if p.state == logic.STATE_SOLD]
        scammed = [p for p in phones if p.state == logic.STATE_SCAMMED]
        return jsonify({
            'total_bought': len(bought),
            'total_sold': len(sold),
            'total_scammed': len(scammed),
            'total_invested': sum(p.buy_price for p in phones),
            'total_revenue': sum(p.sell_price for p in sold if p.sell_price),
            'total_profit': sum((p.sell_price - p.buy_price) for p in sold if p.sell_price) - sum(p.buy_price for p in scammed)
        })

    # Frontend serving (Must be LAST)
    @app.route('/')
    def serve_frontend():
        return send_from_directory(app.static_folder, 'index.html')

    @app.route('/<path:path>')
    def serve_static(path):
        return send_from_directory(app.static_folder, path)
    
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)