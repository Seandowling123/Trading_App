import alpaca_trade_api as tradeapi

API_KEY = 'PKJ8FJYF3MO1MJ8RRMVA'
SECRET_KEY = 'J0WPGzniVtst8W2HK3zaz8ZbQ1Spp5ScZxPqw10x'

# Initialize Alpaca API
api = tradeapi.REST(API_KEY, SECRET_KEY, base_url='https://paper-api.alpaca.markets')

# Place an order
order = api.submit_order(
    symbol='AAPL',
    qty=10,
    side='buy',
    type='market',
    time_in_force='gtc'
)

# Check order status
order_status = order.status
if order_status == 'filled':
    print("Order has been executed successfully.")
    print(f"Average filled price: {order.filled_avg_price}")
else:
    print("Order is still pending or partially filled.")
