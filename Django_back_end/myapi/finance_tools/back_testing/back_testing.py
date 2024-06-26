import numpy as np
import logging
import pandas as pd
import time
from datetime import datetime
import matplotlib.ticker as ticker
from collections import defaultdict
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

# Track position
current_position = 'Sold'
bought_price = None

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
def execute_trades(historical_data, num_std_dev=2):
    close_prices =  list(historical_data['close'])
    
    # check if there is enough data
    if len(close_prices) >= 20:
        global num_trades
        upper_band, lower_band = get_bollinger_bands(close_prices, num_std_dev=num_std_dev)
        
        # Get current trade position
        global current_position
        global bought_price
        latest_price = close_prices[-1]
    
        # Execute buy
        if current_position == 'Sold' and (latest_price <= lower_band):
            #print(f"[{current_time}] Trade available. Last close: {last_close_formatted}, Lower Band: {lower_band_formatted}, "
                #f"Upper Band: {upper_band_formatted}, Current Position: {current_position}")
            order_data = Order('filled', 'buy', 'SPY', 1, latest_price)
            
            # Order status
            if order_data.status  == 'filled':
                num_trades = num_trades+1
                current_position = 'Bought'
                bought_price = latest_price
                #save_trade_to_csv(order_data)
            
        # Execute sell 
        elif current_position == 'Bought' and (latest_price >= upper_band):
            #print(f"[{current_time}] Trade available. Last close: {last_close_formatted}, Lower Band: {lower_band_formatted}, "
                #f"Upper Band: {upper_band_formatted}, Current Position: {current_position}")
            order_data = Order('filled', 'sell', 'SPY', 1, latest_price)
            
            # Order status
            if order_data.status  == 'filled':
                num_trades = num_trades+1
                #save_trade_to_csv(order_data)
                global total_profit
                total_profit = total_profit + order_data.filled_avg_price - bought_price
                current_position = 'Sold'
                bought_price = None

        # No available trades
        #else:
            #print(f"[{current_time}] No trade available. Last close: {last_close_formatted}, Lower Band: {lower_band_formatted}, "
                #f"Upper Band: {upper_band_formatted}, Current Position: {current_position}")

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

# Plot profits over time
def plot_profit(dates, profits):
    plt.figure(figsize=(12, 6))
    for std_dev in profits:
        plt.plot(dates, profits[std_dev], linewidth=1, label=str(std_dev))
    plt.title('Profit Over Time For Trading Algorithm with Different Bollinger Band Standard Deviations')
    plt.xlabel('Date')
    plt.ylabel('Pofit')
    plt.xlabel('Date', fontsize=15, fontname='Times New Roman')
    plt.ylabel('Close', fontsize=15, fontname='Times New Roman')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tick_params(axis='both', which='major', labelsize=12)
    plt.legend(loc='upper left', prop={'family': 'serif', 'size': 12})
    plt.savefig('Profits_over_time_without_loss_avoidance.png', bbox_inches='tight')
    plt.show()

historical_data = get_loaded_historical_data()

# Test the trading strat on historical data
def backtest():
    dates = []
    profits = defaultdict(list)
    std_devs = [1, 1.2, 1.4, 1.6, 1.8, 2, 2.2, 2.4, 2.6, 2.8, 3]
    
    historical_data = get_loaded_historical_data()
    historical_data.iloc[::-1]
    
    historical_data['close'] = historical_data['close'].astype(float)
    grouped = historical_data.groupby(historical_data.index.date)
    
    global total_profit
    global num_trades
    
    # Back test
    for std_dev in std_devs:
        total_profit = 0
        dates = []
        print(f'Testing std deviation: {std_dev}')
        
        # Test each day in the period
        for date, group in (grouped):
            start_profit = total_profit
            num_trades = 0

            # Backtest each individual day
            start_time = time.time()
            for i in range(len(group)):
                elapsed_time = execute_trades(group[:i], num_std_dev=std_dev)
            end_time = time.time()
            
            # Print the results
            elapsed_time = end_time - start_time
            daily_profit = total_profit - start_profit
            dates.append(date)
            profits[std_dev].append(total_profit)
            print(f'\rBacktested date: {date}. Num trades: {num_trades}. Daily profit: {"{:.2f}".format(daily_profit)}. Elapsed time: {"{:.4f}".format(elapsed_time)}', end='', flush=True)
                
        print(f'\nTotal profit for std dev {std_dev}: {total_profit}')
    
    # Plot results
    plot_profit(dates, profits)

backtest()
        