import pandas as pd
import logging
from datetime import datetime
import pytz
import os
from pathlib import Path
from execute_orders import api

BASE_DIR = Path(__file__).resolve().parent.parent
start_balance = 1000

# Convert the string to a datetime object
def get_datetime_from_string(date_string):
    date_format = "%Y-%m-%d-%H:%M"
    datetime_obj = datetime.strptime(date_string, date_format)
    return datetime_obj

# Read a CSV file containing trade data into a pandas DataFrame
def get_trade_history():
    file_path = os.path.join(BASE_DIR, 'finance_tools/Trade_history/Trade_history.csv')
    df = pd.read_csv(file_path)
    #df['datetime'] = df['datetime'].apply(get_datetime_from_string)
    df['datetime'] = pd.to_datetime(df['datetime'])
    
    # Get today's trades
    irish_tz = pytz.timezone('Europe/Dublin')
    now_in_irish_tz = datetime.now(irish_tz)
    filtered_df = df[df['datetime'].dt.date == now_in_irish_tz]
    return filtered_df

# Get the current bought/sold position
def get_current_position():
    file_path = os.path.join(BASE_DIR, 'finance_tools/Trade_history/Trade_history.csv')
    trade_history = pd.read_csv(file_path)
    
    # Get the side of the last placed trade
    if len(trade_history) > 0:
        last_trade = trade_history.iloc[-1]
        if last_trade['side'] == 'buy':
            return 'Bought', last_trade['filled_avg_price']
        elif last_trade['side'] == 'sell':
            return 'Sold', None
        else:
            logging.info(f"Error getting current position")
            return None, None
    else:
        return 'Sold', None

# Get trading acccount details
def get_account_details():
    account = api.get_account()
    account_details = {'start_balance': start_balance, 'portfolio_value': account.portfolio_value, 'current_position': get_current_position()[0]}
    df = pd.DataFrame([account_details])
    return df