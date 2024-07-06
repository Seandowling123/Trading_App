from apscheduler.schedulers.background import BackgroundScheduler
import time
import pandas as pd
import json
import os
from pathlib import Path
from datetime import datetime
import yfinance as yf
import pandas as pd
import psycopg2
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
    
# Check if an asset is available by ticker
def ticker_available(ticker):
    try:
        asset = api.get_asset(ticker)
        if asset and asset.tradable: 
            return True
        return False
    except:
        return False
    
def create_database(dbname, user, password, host, port):
    try:
        # Connect to default PostgreSQL database (e.g., postgres)
        conn = psycopg2.connect(
            dbname="postgres",
            user=user,
            password=password,
            host=host,
            port=port
        )

        conn.autocommit = True
        cursor = conn.cursor()

        # Execute SQL command to create a new database
        create_db_query = f"CREATE DATABASE {dbname};"
        cursor.execute(create_db_query)
        print(f"Database '{dbname}' created successfully")
        
        # Close connection and cursor
        if conn:
            cursor.close()
            conn.close()
            print("PostgreSQL connection is closed")

    except (Exception, psycopg2.Error) as error:
        print(f"Error while connecting to PostgreSQL or creating database '{dbname}':", error)

# Save trading data to PostgrSQL database
def save_trade_to_database(side, client_order_id, symbol, qty, filled_avg_price):
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            dbname="trade_history",
            user="postgres",
            password="test_password",
            host="127.0.0.1",
            port="5432"
        )
        cursor = conn.cursor()
        
        # Insert table
        table_query = """
        CREATE TABLE IF NOT EXISTS trades (
            id SERIAL PRIMARY KEY,
            side VARCHAR(10) NOT NULL,
            client_order_id VARCHAR(50) NOT NULL,
            datetime VARCHAR(20) NOT NULL,
            symbol VARCHAR(20) NOT NULL,
            qty INTEGER NOT NULL,
            filled_avg_price NUMERIC(12, 6) NOT NULL
        );
        """
        cursor.execute(table_query)
        
        # Execute the SQL query
        insert_query = """
        INSERT INTO trades (side, client_order_id, datetime, symbol, qty, filled_avg_price)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        trade_data = (side, client_order_id, current_datetime_string(), symbol, qty, filled_avg_price)
        cursor.execute(insert_query, trade_data)

        # Commit changes to the database
        conn.commit()
        print("Data inserted successfully")
        
        # Close cursor and connection
        if conn:
            cursor.close()
            conn.close()
            print("PostgreSQL connection is closed")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL or inserting data:", error)

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

        # Print the first few rows of the DataFrame
        print(df.head())
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
        print("Error while connecting to PostgreSQL or fetching data for trade history:", error)


# Example usage:
#create_database("trade_history", "postgres", "test_password", "localhost", "5432")
save_trade_to_database('buy', '12345', 'AAPL', 100, 148.25)
print(get_trade_history())