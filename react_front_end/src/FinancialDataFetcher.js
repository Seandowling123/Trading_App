import React, { useState, useEffect } from 'react';
import axios from 'axios';
import StockChart from './Plot_data.js';
import AccountDetails from './account_details.js';

const fetchData = async (url, setData) => {
  try {
    const response = await axios.get(url);
    setData(response.data);
  } catch (error) {
    console.error('Error fetching data:', error);
  }
};

const Get_stock_chart = () => {
  const [historical_data, setHistorical_data] = useState('');
  const [trade_history, setTrade_history] = useState('');
  const [account_details, setAccount_details] = useState('');

  const updateData = () => {
    fetchData('http://127.0.0.1:8000/api/historical_data/SPY', (data) => setHistorical_data(data.financial_data));
    fetchData('http://127.0.0.1:8000/api/trade_history', (data) => setTrade_history(data.trade_history));
    fetchData('http://127.0.0.1:8000/api/account_details', (data) => setAccount_details(data.account_details));
    //fetchData('http://51.20.79.10:8000/api/historical_data/SPY', (data) => setHistorical_data(data.financial_data));
    //fetchData('http://51.20.79.10:8000/api/trade_history', (data) => setTrade_history(data.trade_history));
    //fetchData('http://51.20.79.10:8000/api/account_details', (data) => setAccount_details(data.account_details));
  };

  useEffect(() => {
    updateData();
  }, []);

  return (
    <div id="trade-data-container">
      <button onClick={updateData}>Refresh Data</button>
      <StockChart historical_data={historical_data} markersData={trade_history} />
      <AccountDetails account_details={account_details} />
    </div>
  );
};

export default Get_stock_chart;