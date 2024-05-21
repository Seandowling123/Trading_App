import numpy as np
import time
from apscheduler.schedulers.background import BackgroundScheduler
from get_financial_data import get_close_prices
from execute_orders import buy, sell, get_order_data
import alpaca_trade_api as tradeapi
from API_keys import API_KEY, SECRET_KEY

# Initialize Alpaca API
api = tradeapi.REST(API_KEY, SECRET_KEY, base_url='https://paper-api.alpaca.markets')

# Position tracking
current_position = 'sold'
bought_price = None

# Calculate the bollinger bands for the current data
def get_bollinger_bands(close_prices, window=20, num_std_dev=1.5):
    mean = np.mean(close_prices[-window:])
    std_dev = np.std(close_prices[-window:])
    
    # Calculate the upper and lower bands
    upper_band = mean + num_std_dev * std_dev
    lower_band = mean - num_std_dev * std_dev
    return upper_band, lower_band

# Make the trading decisions
def execute_trades():
    close_prices = list(get_close_prices('SPY'))
    upper_band, lower_band = get_bollinger_bands(close_prices)
    lower_band = 530.02+1
    
    # Make trade decision
    global current_position
    global bought_price
    
    # Execute buy
    if current_position == 'sold' and (close_prices[-1] <= lower_band):
        order_id = buy('SPY', 1)
        order_data = get_order_data(order_id)
        if order_data.status  == 'filled':
            current_position == 'bought'
            bought_price = order_data.filled_avg_price
        print(order_data.status)
        
    # Execute sell 
    elif current_position == 'bought' and (close_prices[-1] >= bought_price) and (close_prices[-1] >= upper_band):
        order_id = sell('SPY', 1)
        order_data = get_order_data(order_id)
        if order_data.status  == 'filled':
            current_position == 'sold'
            bought_price = None
        print(order_data.status)
    else: print('No trade available:', close_prices[-1], lower_band, upper_band)

# Execute trades every minute
def run_trading_algorithm():
    print('Running trading algorithm.')
    scheduler = BackgroundScheduler()

    # Add the job to execute my_function at 1 second past each minute
    scheduler.add_job(execute_trades, 'cron', second='1')
    scheduler.start()

    # Keep the program running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping the scheduler")
        scheduler.shutdown()

def cock():
    get_close_prices('SPY')

run_trading_algorithm()