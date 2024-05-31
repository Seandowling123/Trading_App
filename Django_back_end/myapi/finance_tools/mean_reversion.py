import numpy as np
import logging
import time
import pytz
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from get_financial_data import get_close_prices
from get_trade_history import get_current_position
from execute_orders import buy, sell, get_order_data, save_trade_to_csv, market_open, api

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
    
    # Get current trade position
    current_position, bought_price = get_current_position()
    
    # check if there is enough data
    if len(close_prices) >= 20:
    
        # Execute buy
        if current_position == 'Sold' and (close_prices[-1] <= lower_band):
            order_id = buy('SPY', 1)
            logging.info(f"[{current_time}] Trade available. Last close: {last_close_formatted}, Lower Band: {lower_band_formatted}, "
                  f"Upper Band: {upper_band_formatted}, Current Position: {current_position}")
            order_data = get_order_data(order_id)
            if order_data.status  == 'filled':
                save_trade_to_csv(order_data)
            logging.info(f"Order status: {order_data.status}")
            
        # Execute sell 
        elif current_position == 'Bought' and (close_prices[-1] >= bought_price) and (close_prices[-1] >= upper_band):
            order_id = sell('SPY', 1)
            logging.info(f"[{current_time}] Trade available. Last close: {last_close_formatted}, Lower Band: {lower_band_formatted}, "
                  f"Upper Band: {upper_band_formatted}, Current Position: {current_position}")
            order_data = get_order_data(order_id)
            if order_data.status  == 'filled':
                save_trade_to_csv(order_data)
            logging.info(f"Order status: {order_data.status}")
        else:
            logging.info(f"[{current_time}] No trade available. Last close: {last_close_formatted}, Lower Band: {lower_band_formatted}, "
                  f"Upper Band: {upper_band_formatted}, Current Position: {current_position}")


# Execute trades every minute
def run_trading_algorithm():
    logging.info('Running trading algorithm.')
    scheduler = BackgroundScheduler()
    
    # Check if the market is open
    if market_open():
        
         # Add the job to execute my_function at 1 second past each minute
        scheduler.add_job(execute_trades, 'cron', second='1')
        scheduler.start()
    else:
        clock = api.get_clock()
        eastern = pytz.timezone('EST')
        next_opening_time = clock.next_open.replace(tzinfo=eastern).astimezone(pytz.utc)
        #next_opening_time = datetime(2024,5,29,11,14))
        
        scheduler.add_job(execute_trades, 'date', run_date=next_opening_time)
        logging.info(f"Market is closed. Scheduled to run when the market opens at [{next_opening_time} UTC].")
        
    scheduler.start()

    # Keep the program running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Stopping the scheduler")
        scheduler.shutdown()