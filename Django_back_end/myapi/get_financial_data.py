import requests

def get_historical_stock_data(symbol, api_key):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"

    try:
        response = requests.get(url)
        data = response.json()

        if "Time Series (Daily)" in data:
            return data["Time Series (Daily)"]
        else:
            print("Error: Unable to fetch data")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# Example usage
if __name__ == "__main__":
    symbol = "AAPL"  # Example stock symbol (Apple Inc.)
    api_key = "YOUR_API_KEY"  # Replace with your Alpha Vantage API key

    stock_data = get_historical_stock_data(symbol, api_key)
    if stock_data:
        print("Historical Stock Data:")
        for date, values in stock_data.items():
            print(f"Date: {date}, Close Price: {values['4. close']}")
