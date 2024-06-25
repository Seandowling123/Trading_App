import numpy as np
import logging
import pandas as pd
import time
from datetime import datetime
import matplotlib.ticker as ticker
from apscheduler.schedulers.background import BackgroundScheduler
import alpaca_trade_api as tradeapi
from get_trade_history import get_current_position
from execute_orders import save_trade_to_csv
import matplotlib.pyplot as plt

API_KEY = 'PKBFUD7W4MK990JB9NGI'
SECRET_KEY = 'GtXXLqUNyDWWnC6lm7oFkazymYXfkmtdVKRgb61J'
api = tradeapi.REST(API_KEY, SECRET_KEY, base_url='https://paper-api.alpaca.markets')

#Track profit
total_profit = 0
num_trades = 0

# Trade order class
class Order:
    def __init__(self, status, side, symbol, qty, filled_avg_price):
        self.status = status
        self.side = side
        self.symbol = symbol
        self.qty = qty
        self.filled_avg_price = filled_avg_price
        self.client_order_id = 0

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
        print(f'Error calculating Bollinger Bands for trade: {e}')
        return None

# Make the trading decisions
def execute_trades(historical_data):
    try:
        global num_trades
        close_prices =  list(historical_data['close'])
        
        # check if there is enough data
        if len(close_prices) >= 20:
            upper_band, lower_band = get_bollinger_bands(close_prices)
            current_time = list(historical_data.index)[-1]
            
            # Format numbers to two decimal places
            last_close_formatted = "{:.2f}".format(close_prices[-1])
            lower_band_formatted = "{:.2f}".format(lower_band)
            upper_band_formatted = "{:.2f}".format(upper_band)
            
            # Get current trade position
            current_position, bought_price = get_current_position()
        
            # Execute buy
            if current_position == 'Sold' and (close_prices[-1] <= lower_band):
                print(f"[{current_time}] Trade available. Last close: {last_close_formatted}, Lower Band: {lower_band_formatted}, "
                    f"Upper Band: {upper_band_formatted}, Current Position: {current_position}")
                order_data = Order('filled', 'buy', 'SPY', 1, close_prices[-1])
                
                # Order status
                if order_data.status  == 'filled':
                    num_trades = num_trades+1
                    save_trade_to_csv(order_data)
                
            # Execute sell 
            elif current_position == 'Bought' and (close_prices[-1] >= bought_price) and (close_prices[-1] >= upper_band):
                print(f"[{current_time}] Trade available. Last close: {last_close_formatted}, Lower Band: {lower_band_formatted}, "
                    f"Upper Band: {upper_band_formatted}, Current Position: {current_position}")
                order_data = Order('filled', 'sell', 'SPY', 1, close_prices[-1])
                
                # Order status
                if order_data.status  == 'filled':
                    num_trades = num_trades+1
                    save_trade_to_csv(order_data)
                    global total_profit
                    total_profit = total_profit + order_data.filled_avg_price - bought_price

            # No available trades
            #else:
                #print(f"[{current_time}] No trade available. Last close: {last_close_formatted}, Lower Band: {lower_band_formatted}, "
                    #f"Upper Band: {upper_band_formatted}, Current Position: {current_position}")
                
    except Exception as e: 
        print(f'Error executing trade: {e}')
        return None


def get_loaded_historical_data():
    data = pd.read_pickle('Django_back_end/myapi/finance_tools/back_testing/spy_minute_data_alpha_vantage.pkl')
    return data

def plot(historical_data):
    historical_data['close'] = historical_data['close'].astype(float)
    grouped = historical_data.groupby(historical_data.index.date)

    for date, group in grouped:
        # Plot data
        plt.figure(figsize=(10, 6))
        plt.plot(group.index, (group['close']), linestyle='-', color='b', marker='o')
        plt.title('Basic Plot for DataFrame Data')
        plt.xlabel('Date')
        plt.ylabel('Value')
        plt.xlabel('Date', fontsize=15, fontname='Times New Roman')
        plt.ylabel('Close', fontsize=15, fontname='Times New Roman')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tick_params(axis='both', which='major', labelsize=12)
        print(group)
        plt.show()
        break

historical_data = get_loaded_historical_data()

# Test the trading strat on historical data
def backtest():
    historical_data = get_loaded_historical_data()
    historical_data.iloc[::-1]
    
    historical_data['close'] = historical_data['close'].astype(float)
    grouped = historical_data.groupby(historical_data.index.date)
    
    global total_profit
    global num_trades
    for date, group in grouped:
        start_profit = total_profit
        num_trades = 0

        # Backtest each individual day
        start_time = time.time()
        for i in range(len(group)):
            elapsed_time = execute_trades(group[:i])
        end_time = time.time()
        
        # Print the results
        elapsed_time = end_time - start_time
        daily_profit = total_profit - start_profit
        print(f'Backtested date: {date}. Num trades: {num_trades}. Daily profit: {daily_profit}. Elapsed time: {elapsed_time}')
            
    print(f'\nTotal profit: {total_profit}')

backtest()
        