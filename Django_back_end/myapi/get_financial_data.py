import yfinance as yf

# Get historical stock data
def get_historical_data(ticker, timescale):
    try:
        print('Retrieving stock data.')
        if timescale == 'day':
            prd = '1d'
            itrvl = '1m'
        elif timescale == 'week':
            prd = '5d'
            itrvl = '1d'
        elif timescale == 'month':
            prd = '1mo'
            itrvl = '1d'
        elif timescale == 'year':
            prd = '1y'
            itrvl = '1d'
            
        # Fetch historical stock data using yfinance
        data = yf.download(ticker, period=prd, interval=itrvl, auto_adjust=True)
        return data
    except Exception as e: 
        print(f'Error getting data for {ticker}: {e}')
        return None

print(get_historical_data('AAPL', 'day'))