import alpaca_trade_api as tradeapi

def get_historical_data(ticker):
    try:
        return api.get_bars(ticker, tradeapi.rest.TimeFrame.Day, "2021-06-08", "2021-06-09", adjustment='raw').df
    except Exception as e: print(f'Error getting data for {ticker}: {e}')

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
        api.submit_order(
        symbol=ticker,
        qty=quantity,
        side='buy',
        type='market',
        time_in_force='gtc')
        print(f'\nTrade Executed: Buy {ticker} x{quantity}.')
    except Exception as e: print(f'Error buying {ticker}: {e}')

# Submit a sell order 
def sell(ticker, quantity):
    try:
        api.submit_order(
        symbol=ticker,
        qty=quantity,
        side='sell',
        type='market',
        time_in_force='gtc')
        print(f'\nTrade Executed: Sell {ticker} x{quantity}.')
    except Exception as e: print(f'Error selling {ticker}: {e}')


API_KEY = 'PKJ8FJYF3MO1MJ8RRMVA'
SECRET_KEY = 'J0WPGzniVtst8W2HK3zaz8ZbQ1Spp5ScZxPqw10x'

api = tradeapi.REST(API_KEY, SECRET_KEY, base_url='https://paper-api.alpaca.markets')

account = api.get_account()
print('Cash:', account.cash)
print('Buying Power:', account.buying_power)

print(get_historical_data('AAPL'))
