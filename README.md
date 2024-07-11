# Trading App Description

## Overview

This trading app features a trading algorithm that uses Bollinger Bands to generate trade signals. The application collects live historical data using the `yfinance` library and executes trades using the Alpaca API. The algorithm is currently focused on trading the S&P 500 ticker, SPY.

## Features

- **Trading Algorithm**: Uses Bollinger Bands to determine buy and sell signals.
- **Live Data Collection**: Fetches real-time historical data via the `yfinance` library.
- **Trade Execution**: Executes trades through the Alpaca API.
- **Hosting**: The application is currently hosted on an AWS EC2 instance.
- **Backend**: Built with Django and Nginx, the backend supplies live activity and performance data.
- **Frontend**: A React.js-based dashboard available at [seand.ie](https://seand.ie) for monitoring trading activity and performance metrics.

## Technical Stack

- **Python**: Core language for the trading algorithm & backend.
- **yfinance**: Library used for fetching live historical data.
- **Alpaca API**: Used for executing trades.
- **PostgreSQL**: Database to save and retrieve trading activity.
- **Django**: Framework for the backend.
- **Nginx**: Web server and reverse proxy for the backend.
- **React.js**: Framework for the frontend dashboard.
- **AWS EC2**: Hosting platform for the application.

## Dashboard

The frontend dashboard, created using React.js, provides real-time data on the trading algorithm’s performance and activity. The dashboard is viewable [seand.ie](https://seand.ie). An example capture of the dashboard is shown below.

![dashboard](https://github.com/Seandowling123/Trading_App/assets/61026772/4b8bd7e2-9373-48c5-b172-97c62ec72d49)


## Compliance

Note that the algorithm currently operates on a paper trading account with a high balance for compliance with [trading regulations](https://www.investopedia.com/terms/p/patterndaytrader.asp).
