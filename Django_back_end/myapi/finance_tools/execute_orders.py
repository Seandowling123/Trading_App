from datetime import datetime
import alpaca_trade_api as tradeapi
from API_keys import API_KEY, SECRET_KEY

# Create a string of the current date and time
def current_datetime_string():
    return datetime.now().strftime('%Y-%m-%d-%H:%M')

# Create an order ID
def get_order_id(ticker, side):
    return f'{side}-{ticker}-{current_datetime_string()}'

# Check if an asset is available by ticker
def ticker_available(ticker):
    try:
        asset = api.get_asset(ticker)
        if asset and asset.tradable: 
            return True
        return False
    except:
        return False

# Submit a buy order
def buy(ticker, quantity):
    try:
        order = api.submit_order(
        symbol=ticker,
        qty=quantity,
        side='buy',
        type='market',
        time_in_force='fok',
        client_order_id=get_order_id(ticker, 'buy'))
        print(f'Order Submitted: Buy {ticker} x{quantity}.')
        return order.client_order_id
    except Exception as e: print(f'Error buying {ticker}: {e}')

# Submit a sell order 
def sell(ticker, quantity):
    try:
        order = api.submit_order(
        symbol=ticker,
        qty=quantity,
        side='sell',
        type='market',
        time_in_force='fok',
        client_order_id=get_order_id(ticker, 'sell'))
        print(f'Order Submitted: Sell {ticker} x{quantity}.')
        return order.client_order_id
    except Exception as e: print(f'Error selling {ticker}: {e}')
    
# Get the status of an order after its been submitted
def get_order_data(order_id):
    order_data = api.get_order_by_client_order_id(order_id)
    return order_data

# Get previous order data
def get_prev_orders():
    order_chunk = api.list_orders(status='all', 
                                    nested='False', 
                                    direction='desc',)
    return order_chunk

api = tradeapi.REST(API_KEY, SECRET_KEY, base_url='https://paper-api.alpaca.markets')

account = api.get_account()
print('Cash:', account.cash)
print('Buying Power:', account.buying_power)
