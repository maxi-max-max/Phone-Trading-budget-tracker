from models import Phone, Budget
from database import db
from datetime import datetime

# --- Constants (Removes Hardcoded Values) ---
STATE_BOUGHT = 'bought'
STATE_SOLD = 'sold'
STATE_SCAMMED = 'scammed'

MSG_SUCCESS = 'success'
MSG_WARNING = 'warning'
MSG_INFO = 'info'
MSG_ERROR = 'error'

THRESHOLD_CHEAP = 200
THRESHOLD_EXPENSIVE = 800

# --- Business Logic ---

def get_or_create_budget():
    """Ensures a budget record always exists."""
    budget = Budget.query.first()
    if not budget:
        budget = Budget(total_money=0.0)
        db.session.add(budget)
        db.session.commit()
    return budget

def update_budget_transaction(amount):
    """Updates budget safely."""
    budget = get_or_create_budget()
    budget.total_money += amount
    budget.updated_at = datetime.utcnow()
    # Note: Commit happens in the calling function to ensure atomicity

def evaluate_deal(phone, action_type):
    """Analyzes the deal and returns UI messages."""
    messages = []
    
    if action_type == 'buy':
        if phone.buy_price < THRESHOLD_CHEAP:
            messages.append({
                'type': MSG_SUCCESS,
                'message': f'Great deal! {phone.brand} {phone.model} is below market average.'
            })
        elif phone.buy_price > THRESHOLD_EXPENSIVE:
            messages.append({
                'type': MSG_WARNING,
                'message': f'High investment! Ensure high resale value for {phone.brand} {phone.model}.'
            })
        else:
            messages.append({
                'type': MSG_INFO,
                'message': f'Fair price for {phone.brand} {phone.model}.'
            })
    
    elif action_type == 'sell' and phone.sell_price:
        profit = phone.sell_price - phone.buy_price
        profit_percentage = (profit / phone.buy_price) * 100
        
        if profit_percentage > 30:
            messages.append({
                'type': MSG_SUCCESS,
                'message': f'Excellent! ${profit:.2f} ({profit_percentage:.1f}%) profit.'
            })
        elif profit > 0:
            messages.append({
                'type': MSG_INFO,
                'message': f'Small profit of ${profit:.2f}.'
            })
        else:
            messages.append({
                'type': MSG_WARNING,
                'message': f'Loss of ${abs(profit):.2f}. Review strategy.'
            })
    
    elif action_type == 'scam':
        messages.append({
            'type': MSG_ERROR,
            'message': f'Lost ${phone.buy_price} to a scam.'
        })
    
    return messages

def handle_state_change(phone, new_state, sell_price=None):
    """
    Handles complex logic of changing states and updating budget.
    Returns: messages list
    """
    old_state = phone.state
    messages = []
    
    # 1. Handle Budget Updates
    if old_state == STATE_BOUGHT and new_state == STATE_SOLD:
        phone.sell_price = float(sell_price)
        update_budget_transaction(phone.sell_price)
        messages = evaluate_deal(phone, 'sell')

    elif old_state == STATE_SOLD and new_state == STATE_SCAMMED:
        # Revoke the money we thought we made
        if phone.sell_price:
            update_budget_transaction(-phone.sell_price)
        messages = evaluate_deal(phone, 'scam')

    elif old_state == STATE_BOUGHT and new_state == STATE_SCAMMED:
        messages = evaluate_deal(phone, 'scam')

    elif old_state == STATE_SCAMMED and new_state == STATE_SOLD:
        phone.sell_price = float(sell_price)
        update_budget_transaction(phone.sell_price)
        messages = evaluate_deal(phone, 'sell')

    # 2. Update Phone
    phone.state = new_state
    phone.updated_at = datetime.utcnow()
    
    return messages