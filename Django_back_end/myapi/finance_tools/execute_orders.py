import alpaca_trade_api as tradeapi
from API_keys import API_KEY, SECRET_KEY

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
        time_in_force='fok')
        print(f'Order Submitted: Buy {ticker} x{quantity}.')
        return order.id
    except Exception as e: print(f'Error buying {ticker}: {e}')

# Submit a sell order 
def sell(ticker, quantity):
    try:
        order = api.submit_order(
        symbol=ticker,
        qty=quantity,
        side='sell',
        type='market',
        time_in_force='fok')
        print(f'Order Submitted: Sell {ticker} x{quantity}.')
        return order.id
    except Exception as e: print(f'Error selling {ticker}: {e}')

api = tradeapi.REST(API_KEY, SECRET_KEY, base_url='https://paper-api.alpaca.markets')

account = api.get_account()
print('Cash:', account.cash)
print('Buying Power:', account.buying_power)
