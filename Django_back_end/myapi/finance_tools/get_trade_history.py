import pandas as pd
import logging
import psycopg2
from datetime import datetime
import pytz
import os
from pathlib import Path
from .execute_orders import api

BASE_DIR = Path(__file__).resolve().parent.parent
start_balance = 100000

# Convert the string to a datetime object
def get_datetime_from_string(date_string):
    date_format = "%Y-%m-%d-%H:%M"
    datetime_obj = datetime.strptime(date_string, date_format)
    return datetime_obj

# Get trade history from PostgrSQL database
def get_trade_history():
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            dbname="trade_history",
            user="postgres",
            password="test_password",
            host="127.0.0.1",
            port="5432"
        )

        # Load data into Pandas DataFrame
        query = "SELECT * FROM trades;"
        df = pd.read_sql_query(query, conn)
        df['datetime'] = pd.to_datetime(df['datetime'])
        
        # Get today's trades
        irish_tz = pytz.timezone('Europe/Dublin')
        now_in_irish_tz = datetime.now(irish_tz).date()
        filtered_df = df[df['datetime'].dt.date == now_in_irish_tz]
        
        # Close the connection
        if conn:
            conn.close()
        return filtered_df
    except (Exception, psycopg2.Error) as error:
        logging.info("Error while connecting to PostgreSQL or fetching data for trade history:", error)

# Get the current bought/sold position
def get_current_position():
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            dbname="trade_history",
            user="postgres",
            password="test_password",
            host="127.0.0.1",
            port="5432"
        )

        # Load data into Pandas DataFrame
        query = "SELECT * FROM trades;"
        trade_history = pd.read_sql_query(query, conn)
        
        # Close the connection
        if conn:
            conn.close()
        
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
    except (Exception, psycopg2.Error) as error:
        logging.info("Error while connecting to PostgreSQL or fetching data for current position:", error)

# Get trading acccount details
def get_account_details():
    account = api.get_account()
    account_details = {'start_balance': start_balance, 'portfolio_value': account.portfolio_value, 'current_position': get_current_position()[0]}
    df = pd.DataFrame([account_details])
    return df