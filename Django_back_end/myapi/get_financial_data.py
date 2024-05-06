import yfinance as yf
import pandas as pd

# Get historical stock data
def get_historical_data(ticker, timescale):
    try:
        print('\nRetrieving stock data.')
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

# Calculate Bollinger Bands
def calculate_bollinger_bands(close, window_size=20, num_std_dev=1.8):
    rolling_mean = close.rolling(window=window_size).mean()
    rolling_std = close.rolling(window=window_size).std()

    # Calculate upper and lower Bollinger Bands
    upper_band = rolling_mean + num_std_dev * rolling_std
    lower_band = rolling_mean - num_std_dev * rolling_std
    return upper_band, lower_band

# Return close price time series with Bollinger Bands
def get_close_with_bands(ticker, timescale='day'):
    data = get_historical_data(ticker, timescale)
    close = data['Close']
    upper_band, lower_band = calculate_bollinger_bands(close)
    dataframe = pd.DataFrame({'Price': close, 'Upper Band': upper_band, 'Lower Band': lower_band})
    dataframe.reset_index(inplace=True)
    dataframe.rename(columns={'index': 'date'}, inplace=True)
    return dataframe[20:]

#get_close_with_bands('AAPL')