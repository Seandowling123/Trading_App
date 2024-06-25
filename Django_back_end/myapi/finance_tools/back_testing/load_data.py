import pandas as pd

def get_loaded_historical_data():
    data = pd.read_pickle('Django_back_end/myapi/finance_tools/back_testing/spy_minute_data_alpha_vantage.pkl')
    return data

data = get_loaded_historical_data()
print(data.head())
print(data.tail())
print(len(data))
