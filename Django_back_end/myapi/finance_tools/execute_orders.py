from datetime import datetime
import time
import csv
import json
import os
from pathlib import Path
import alpaca_trade_api as tradeapi
from API_keys import API_KEY, SECRET_KEY

BASE_DIR = Path(__file__).resolve().parent.parent

# Create a string of the current date and time
def current_datetime_string():
    return datetime.now().strftime('%Y-%m-%d-%H:%M')

# Create an order ID
def get_order_id(ticker, side):
    return f'{side}-{ticker}-{current_datetime_string()}'

# Save order details to CSV
def save_trade_to_csv(order_data, csv_path=os.path.join(BASE_DIR, 'finance_tools/Trade_history\Trade_history.csv')):
    fieldnames = ['side', 'client_order_id', 'datetime', 'symbol', 'qty', 'filled_avg_price']

    # Check if the CSV file already exists
    file_exists = Path(csv_path).exists()

    with open(csv_path, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write headers if the file is newly created
        if not file_exists:
            writer.writeheader()

        # Write order data to the CSV file
        writer.writerow({
            'side': order_data.side,
            'client_order_id': order_data.client_order_id,
            'datetime': current_datetime_string(),
            'symbol': order_data.symbol,
            'qty': order_data.qty,
            'filled_avg_price': order_data.filled_avg_price
        })
        
# Save order details to JSON
def save_trade_to_json(order_data, json_path=os.path.join(BASE_DIR, 'finance_tools/Trade_history/Trade_history.json')):
    json_path = Path(json_path)
    
    # Load existing data if the JSON file exists
    if json_path.exists():
        with open(json_path, 'r') as file:
            data = json.load(file)
    else:
        data = []

    # Append the new order data
    new_entry = {
        'side': order_data.side,
        'client_order_id': order_data.client_order_id,
        'datetime': current_datetime_string(),
        'symbol': order_data.symbol,
        'qty': order_data.qty,
        'filled_avg_price': order_data.filled_avg_price
    }
    data.append(new_entry)

    # Write the updated data back to the JSON file
    with open(json_path, 'w') as file:
        json.dump(data, file, indent=4)

# Check if an asset is available by ticker
def ticker_available(ticker):
    try:
        asset = api.get_asset(ticker)
        if asset and asset.tradable: 
            return True
        return False
    except:
        return False

# Submit a buy order
def buy(ticker, quantity):
    try:
        order = api.submit_order(
            symbol=ticker,
            qty=quantity,
            side='buy',
            type='market',
            time_in_force='fok',
            client_order_id=get_order_id(ticker, 'Buy')
        )
        print(f"Order successfully submitted:\n"
              f"    - Side: Buy\n"
              f"    - Ticker: {ticker}\n"
              f"    - Quantity: {quantity}\n"
              f"    - Order ID: {order.client_order_id}\n"
              f"    - Created at: {order.created_at}\n"
        )
        return order.client_order_id
    except Exception as e: print(f'Error buying {ticker}: {e}')

# Submit a sell order 
def sell(ticker, quantity):
    try:
        order = api.submit_order(
            symbol=ticker,
            qty=quantity,
            side='sell',
            type='market',
            time_in_force='fok',
            client_order_id=get_order_id(ticker, 'Sell')
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
    
# Get data about an order from its ID
def get_order_data(order_id, initial_delay=2, polling_interval=2, timeout=30):
    order_data = api.get_order_by_client_order_id(order_id)
    
    # Ensure order has been processed
    if order_data.status == 'new':
        time.sleep(initial_delay)
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            order_data = get_order_data(order_id)
            if order_data.status != 'new':
                return order_data
            time.sleep(polling_interval)
        return None
    return order_data

# Get previous order data
def get_prev_orders():
    order_chunk = api.list_orders(status='all', 
                                    nested='False', 
                                    direction='desc',)
    return order_chunk

api = tradeapi.REST(API_KEY, SECRET_KEY, base_url='https://paper-api.alpaca.markets')

account = api.get_account()
print('Cash:', account.cash)
print('Buying Power:', account.buying_power)
