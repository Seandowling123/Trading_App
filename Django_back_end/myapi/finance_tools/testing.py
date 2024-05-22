from apscheduler.schedulers.background import BackgroundScheduler
import time
from get_financial_data import get_close_prices
import pandas as pd
import json
import os
from pathlib import Path
from execute_orders import buy, sell, get_prev_orders
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent

def current_datetime_string():
    return datetime.now().strftime('%Y-%m-%d %H:%M')

def my_function():
    print(get_close_prices('SPY'))
    print("Executing my function at 1 second past the minute")
    
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


def schedule():
    # Create a scheduler
    scheduler = BackgroundScheduler()

    # Add the job to execute my_function at 1 second past each minute
    scheduler.add_job(my_function, 'cron', second='1')

    # Start the scheduler
    scheduler.start()

    # Keep the program running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping the scheduler")
        scheduler.shutdown()

from datetime import datetime

# Your string
date_string = "2024-05-21-15:02"

# Convert the string to a datetime object
date_format = "%Y-%m-%d-%H:%M"
datetime_obj = datetime.strptime(date_string, date_format)

# Print the datetime object
print(datetime_obj)
