import numpy as np
import logging
import time
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .get_financial_data import get_close_prices
from .get_trade_history import get_current_position, get_buy_qantity
from .execute_orders import buy, sell, get_order_data, save_trade_to_database, market_open, api

# Calculate the bollinger bands for the current data
def get_bollinger_bands(close_prices, window=20, num_std_dev=2):
    try:
        mean = np.mean(close_prices[-window:])
        std_dev = np.std(close_prices[-window:])
        
        # Calculate the upper and lower bands
        upper_band = mean + num_std_dev * std_dev
        lower_band = mean - num_std_dev * std_dev
        return upper_band, lower_band
    except Exception as e: 
        logging.info(f'Error calculating Bollinger Bands for trade: {e}')
        return None

# Make the trading decisions
def execute_trades():
    try:
        close_prices = list(get_close_prices('SPY'))
        upper_band, lower_band = get_bollinger_bands(close_prices)
        current_time = datetime.now().strftime("%d/%b/%Y %H:%M:%S")
        
        # Format numbers to two decimal places
        last_close_formatted = "{:.2f}".format(close_prices[-1])
        lower_band_formatted = "{:.2f}".format(lower_band)
        upper_band_formatted = "{:.2f}".format(upper_band)
        
        # Get current trade position
        current_position, bought_price, bought_quantity = get_current_position()
        latest_close = close_prices[-1]
        
        # check if there is enough data
        if len(close_prices) >= 20:
        
            # Execute buy
            if current_position == 'Sold' and (latest_close <= lower_band):
                buy_qantity = get_buy_qantity()
                order_id = buy('SPY', buy_qantity)
                logging.info(f"[{current_time}] Trade available. Last close: {last_close_formatted}, Lower Band: {lower_band_formatted}, "
                    f"Upper Band: {upper_band_formatted}, Current Position: {current_position}")
                order_data = get_order_data(order_id)
                
                # Order status
                logging.info(f"Order status: {order_data.status}")
                if order_data.status  == 'filled':
                    logging.info('Order filled.')
                    save_trade_to_database(order_data)
                
            # Execute sell 
            elif current_position == 'Bought' and (latest_close >= bought_price) and (latest_close >= upper_band):
                order_id = sell('SPY', int(bought_quantity))
                logging.info(f"[{current_time}] Trade available. Last close: {last_close_formatted}, Lower Band: {lower_band_formatted}, "
                    f"Upper Band: {upper_band_formatted}, Current Position: {current_position}")
                order_data = get_order_data(order_id)
                
                # Order status
                logging.info(f"Order status: {order_data.status}")
                if order_data.status  == 'filled':
                    save_trade_to_database(order_data)
            
            # No available trades
            else:
                logging.info(f"[{current_time}] No trade available. Last close: {last_close_formatted}, Lower Band: {lower_band_formatted}, "
                    f"Upper Band: {upper_band_formatted}, Current Position: {current_position}")
                        
    except Exception as e: 
        logging.info(f'Error executing trade: {e}')
        return None

# Execute trades every minute
def run_trading_algorithm():
    logging.info('Running trading algorithm.')
    scheduler = BackgroundScheduler()
    
    # Check if the market is open
    if market_open():
        
         # Add the job to execute my_function at 1 second past each minute
        scheduler.add_job(execute_trades, 'cron', second='1')
    else:
        clock = api.get_clock()
        next_opening_time = clock.next_open.astimezone('Europe/Dublin')
        #next_opening_time = datetime(2024,5,29,11,14))
        
        scheduler.add_job(run_trading_algorithm, 'date', run_date=next_opening_time)
        logging.info(f"Market is closed. Scheduled to run when the market opens at [{next_opening_time} Dublin time].")
        
    scheduler.start()

    # Keep the program running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Stopping the scheduler")
        scheduler.shutdown()
        