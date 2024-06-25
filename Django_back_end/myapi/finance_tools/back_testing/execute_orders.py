from datetime import datetime
import pytz
import logging
import time
import csv
import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Create a string of the current date and time in Irish Time
def current_datetime_string():
    irish_tz = pytz.timezone('Europe/Dublin')
    now_in_irish_tz = datetime.now(irish_tz)
    return now_in_irish_tz.strftime('%Y-%m-%d-%H:%M %Z')

# Create an order ID
def get_order_id(ticker, side):
    return f'{side}-{ticker}-{current_datetime_string()}'

# Save order details to CSV
def save_trade_to_csv(order_data, csv_path=os.path.join(BASE_DIR, 'back_testing/Trade_history/Trade_history.csv')):
    fieldnames = ['side', 'client_order_id', 'datetime', 'symbol', 'qty', 'filled_avg_price']
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)

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
def save_trade_to_json(order_data, json_path=os.path.join(BASE_DIR, 'back_testing/Trade_history/Trade_history.csv')):
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
