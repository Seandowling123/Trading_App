import alpaca_trade_api as tradeapi
from API_keys import API_KEY, SECRET_KEY

print(API_KEY)

# Initialize Alpaca API
api = tradeapi.REST(API_KEY, SECRET_KEY, base_url='https://paper-api.alpaca.markets')

order_list = api.list_orders(status='closed')

order_id='test_order'
specific_order = api.get_order(order_id)
print(specific_order)

"""# Place an order
order = api.submit_order(
    symbol='AAPL',
    qty=10,
    side='buy',
    type='market',
    time_in_force='gtc',
    client_order_id='test_order'
)"""

"""# Check order status
order_status = order.status
if order_status == 'filled':
    print("Order has been executed successfully.")
    print(f"Average filled price: {order.filled_avg_price}")
else:
    print("Order is still pending or partially filled.")"""
