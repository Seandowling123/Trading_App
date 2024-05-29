import numpy as np
import time
import pytz
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .get_financial_data import get_close_prices
from .execute_orders import buy, sell, get_order_data, save_trade_to_csv, market_open, api

# Position tracking
current_position = 'Sold'
#current_position = 'Bought'
bought_price = None

# Calculate the bollinger bands for the current data
def get_bollinger_bands(close_prices, window=20, num_std_dev=2):
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
    current_time = datetime.now().strftime("%d/%b/%Y %H:%M:%S")
    
    # Format numbers to two decimal places
    last_close_formatted = "{:.2f}".format(close_prices[-1])
    lower_band_formatted = "{:.2f}".format(lower_band)
    upper_band_formatted = "{:.2f}".format(upper_band)
    
    # Make trade decision
    global current_position
    global bought_price
    
    # check if there is enough data
    if len(close_prices) >= 20:
    
        # Execute buy
        if current_position == 'Sold' and (close_prices[-1] <= lower_band):
            order_id = buy('SPY', 1)
            print(f"[{current_time}] Trade available. Last close: {last_close_formatted}, Lower Band: {lower_band_formatted}, "
                  f"Upper Band: {upper_band_formatted}, Current Position: {current_position}")
            order_data = get_order_data(order_id)
            if order_data.status  == 'filled':
                current_position = 'Bought'
                bought_price = float(order_data.filled_avg_price)
                save_trade_to_csv(order_data)
            print(f"Order status: {order_data.status}")
            
        # Execute sell 
        elif current_position == 'Bought' and (close_prices[-1] >= bought_price) and (close_prices[-1] >= upper_band):
            order_id = sell('SPY', 1)
            print(f"[{current_time}] Trade available. Last close: {last_close_formatted}, Lower Band: {lower_band_formatted}, "
                  f"Upper Band: {upper_band_formatted}, Current Position: {current_position}")
            order_data = get_order_data(order_id)
            if order_data.status  == 'filled':
                current_position = 'Sold'
                bought_price = None
                save_trade_to_csv(order_data)
            print(f"Order status: {order_data.status}")
        else:
            print(f"[{current_time}] No trade available. Last close: {last_close_formatted}, Lower Band: {lower_band_formatted}, "
                  f"Upper Band: {upper_band_formatted}, Current Position: {current_position}")


# Execute trades every minute
def run_trading_algorithm():
    print('Running trading algorithm.')
    scheduler = BackgroundScheduler()
    
    # Check if the market is open
    if market_open():
        print("Market is currently open.")
        
         # Add the job to execute my_function at 1 second past each minute
        scheduler.add_job(execute_trades, 'cron', second='1')
        scheduler.start()
    else:
        clock = api.get_clock()
        eastern = pytz.timezone('EST')
        next_opening_time = clock.next_open.replace(tzinfo=eastern).astimezone(pytz.utc)
        #next_opening_time = datetime(2024,5,29,11,14)
        print(next_opening_time)
        
        scheduler.add_job(execute_trades, 'date', run_date=next_opening_time)
        print(f"Market is closed. Scheduled to run when the market opens at [{next_opening_time} UTC].")
        
    scheduler.start()

    # Keep the program running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping the scheduler")
        scheduler.shutdown()
        
run_trading_algorithm()