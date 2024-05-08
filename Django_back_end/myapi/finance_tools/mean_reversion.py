import threading
import time
import schedule
import numpy as np
from get_financial_data import get_close_prices
from execute_orders import buy, sell
import alpaca_trade_api as tradeapi
from API_keys import API_KEY, SECRET_KEY

# Initialize Alpaca API
api = tradeapi.REST(API_KEY, SECRET_KEY, base_url='https://paper-api.alpaca.markets')

current_position = 'sold'

# Calculate the bollinger bands for the current data
def get_bollinger_bands(close_prices, window=20, num_std_dev=1.5):
    mean = np.mean(close_prices[-window:])
    std_dev = np.std(close_prices[-window:])
    
    # Calculate the upper and lower bands
    upper_band = mean + num_std_dev * std_dev
    lower_band = mean - num_std_dev * std_dev
    return upper_band, lower_band

# Get the status of an order after its been submitted
def get_order_status(order_id):
    specific_order = api.get_order_by_client_order_id(order_id)
    print(specific_order)

# Make the trading decisions
def execute_trades():
    close_prices = get_close_prices('SPY')
    upper_band, lower_band = get_bollinger_bands(close_prices)
    
    # Make trade decision
    global current_position
    if current_position == 'sold' and (close_prices[-1] <= lower_band):
        order_id = buy('SPY', 1)
        order_status = get_order_status(order_id)
    elif current_position == 'bought' and (close_prices[-1] >= upper_band):
        order_id = sell('SPY', 1)
        order_status = get_order_status(order_id)
    else: print('No trade available')

# Execute trades every minute
def run_algorithm():
    schedule.every().minute.at(":20").do(execute_trades)

    # Run the scheduler
    while True:
        schedule.run_pending()
        time.sleep(1)
        
trading_thread = threading.Thread(target=run_algorithm)
trading_thread.start()
close_prices = get_close_prices('SPY')