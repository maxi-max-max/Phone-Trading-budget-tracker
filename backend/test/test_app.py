import json

def test_budget_initialization(client):
    """Test that budget starts at 0 or is created automatically."""
    res = client.get('/api/budget')
    assert res.status_code == 200
    assert res.json['total_money'] == 0.0

def test_add_phone_flow(client):
    """Integration test: Add phone, check budget, check state."""
    # 1. Set Budget
    client.post('/api/budget', json={'total_money': 1000})
    
    # 2. Add Phone
    phone_data = {
        'model': 'iPhone 13',
        'brand': 'Apple',
        'buy_price': 600,
        'notes': 'Test'
    }
    res = client.post('/api/phones', json=phone_data)
    assert res.status_code == 200
    assert res.json['phone']['model'] == 'iPhone 13'
    
    # 3. Check Budget (1000 - 600 = 400)
    budget_res = client.get('/api/budget')
    assert budget_res.json['total_money'] == 400.0

def test_sell_phone_profit(client):
    """Test selling a phone updates budget and calculates profit."""
    # Buy
    client.post('/api/budget', json={'total_money': 1000})
    res_buy = client.post('/api/phones', json={
        'model': 'Pixel 6',
        'brand': 'Google',
        'buy_price': 500
    })
    phone_id = res_buy.json['phone']['id']
    
    # Sell
    res_sell = client.put(f'/api/phones/{phone_id}/state', json={
        'state': 'sold',
        'sell_price': 700
    })
    
    assert res_sell.status_code == 200
    assert "profit" in str(res_sell.json['messages'])
    
    # Check Budget (1000 - 500 + 700 = 1200)
    budget_res = client.get('/api/budget')
    assert budget_res.json['total_money'] == 1200.0