from apscheduler.schedulers.background import BackgroundScheduler
import time
import pandas as pd
import json
import os
from pathlib import Path
from datetime import datetime
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from datetime import datetime
import pytz
import logging
import alpaca_trade_api as tradeapi
from API_keys import API_KEY, SECRET_KEY

BASE_DIR = Path(__file__).resolve().parent.parent
api = tradeapi.REST(API_KEY, SECRET_KEY, base_url='https://paper-api.alpaca.markets')

def current_datetime_string():
    return datetime.now().strftime('%Y-%m-%d %H:%M')
    
def load_trade_data_as_dataframe(json_path):
    # Initialize the path
    json_path = Path(json_path)

    # Load the JSON data from the file
    if json_path.exists():
        with open(json_path, 'r') as file:
            data = json.load(file)
        
        # Convert the JSON data to a pandas DataFrame
        df = pd.DataFrame(data)
        return df
    else:
        print(f"The file {json_path} does not exist.")
        return pd.DataFrame()  # Return an empty DataFrame if the file doesn't exist

# Submit a sell order 
def sell(ticker, quantity):
    try:
        order = api.submit_order(
            symbol=ticker,
            qty=quantity,
            side='sell',
            type='market',
            time_in_force='fok'
        )
        print(f"Order successfully submitted:\n"
              f"    - Side: Sell\n"
              f"    - Ticker: {ticker}\n"
              f"    - Quantity: {quantity}\n"
              f"    - Order ID: {order.client_order_id}\n"
              f"    - Created at: {order.created_at}\n"
        )
        return order.client_order_id
    except Exception as e: print(f'Error selling {ticker}: {e}')
    
sell('SPY', 1)