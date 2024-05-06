import alpaca_trade_api as tradeapi
from datetime import datetime, timedelta

# Return a date interval of now and a date delta days ago
def get_dates(delta):
    current_date = datetime.now() - timedelta(days=1)
    date_30_days_ago = current_date - timedelta(days=delta)
    return [date_30_days_ago.strftime('%Y-%m-%d'), current_date.strftime('%Y-%m-%d')]

# Get historical stock data
def get_historical_data(ticker, timescale):
    try:
        if timescale == 'week':
            dates = get_dates(7)
            interval = tradeapi.rest.TimeFrame.Day
        elif timescale == 'month':
            dates = get_dates(30)
            interval = tradeapi.rest.TimeFrame.Day
        elif timescale == 'year':
            dates = get_dates(365)
            interval = tradeapi.rest.TimeFrame.Day
        return api.get_bars(ticker, interval, dates[0], dates[1], adjustment='raw').df
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
        print(f'\Order Submitted: Buy {ticker} x{quantity}.')
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
        print(f'\Order Submitted: Sell {ticker} x{quantity}.')
    except Exception as e: print(f'Error selling {ticker}: {e}')


API_KEY = 'PKJ8FJYF3MO1MJ8RRMVA'
SECRET_KEY = 'J0WPGzniVtst8W2HK3zaz8ZbQ1Spp5ScZxPqw10x'

api = tradeapi.REST(API_KEY, SECRET_KEY, base_url='https://paper-api.alpaca.markets')

account = api.get_account()
print('Cash:', account.cash)
print('Buying Power:', account.buying_power)
