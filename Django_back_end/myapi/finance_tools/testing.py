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

BASE_DIR = Path(__file__).resolve().parent.parent

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

itrvl = '1m'
previous_day = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
previous_day_data = yf.download('SPY', start=previous_day, end=datetime.now().strftime('%Y-%m-%d'), interval=itrvl, auto_adjust=True, progress=False)
last_20_previous_day = previous_day_data.tail(20-5)
print(last_20_previous_day)