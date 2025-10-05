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