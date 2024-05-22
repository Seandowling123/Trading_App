import pandas as pd
from datetime import datetime
import os
from pathlib import Path
from mean_reversion import current_position
from execute_orders import api

BASE_DIR = Path(__file__).resolve().parent.parent

# Convert the string to a datetime object
def get_datetime_from_string(date_string):
    date_format = "%Y-%m-%d-%H:%M"
    datetime_obj = datetime.strptime(date_string, date_format)
    return datetime_obj

# Read a CSV file containing trade data into a pandas DataFrame
def get_trade_history():
    file_path = os.path.join(BASE_DIR, 'finance_tools/Trade_history/Trade_history.csv')
    df = pd.read_csv(file_path)
    df['datetime'] = df['datetime'].apply(get_datetime_from_string)  
    return df

# Get trading acccount details
def get_account_details():
    account = api.get_account()
    return {'portfolio_value': account.portfolio_value, 'current_position': current_position}
