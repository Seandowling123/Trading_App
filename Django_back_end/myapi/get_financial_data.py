import yfinance as yf
from datetime import datetime, timedelta

# Return a date interval of now and a date delta days ago
def get_dates(delta):
    current_date = datetime.now()
    date_30_days_ago = current_date - timedelta(days=delta)
    return [date_30_days_ago.strftime('%Y-%m-%d'), current_date.strftime('%Y-%m-%d')]

# Get historical stock data
def get_historical_data(ticker, timescale):
    try:
        print('Retrieving stock data.')
        if timescale == 'week':
            dates = get_dates(7)
        elif timescale == 'month':
            dates = get_dates(30)
        elif timescale == 'year':
            dates = get_dates(365)
            
        # Fetch historical stock data using yfinance
        data = yf.download(ticker, dates[0], end=None)
        return data
    except Exception as e: 
        print(f'Error getting data for {ticker}: {e}')
        return None
