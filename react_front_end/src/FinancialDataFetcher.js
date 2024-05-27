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
    fetchData('https://seand.ie/api/historical_data/SPY', (data) => setHistorical_data(data.financial_data));
    fetchData('https://seand.ie/api/trade_history', (data) => setTrade_history(data.trade_history));
    fetchData('https://seand.ie/api/account_details', (data) => setAccount_details(data.account_details));
  };

  useEffect(() => {
    updateData();
  }, []);

  return (
    <div id="trade-data-container">
      <StockChart historical_data={historical_data} markersData={trade_history} />
      <div>
        <button className="refresh-button" onClick={updateData}>Refresh</button>
        <AccountDetails account_details={account_details} />
      </div>
      
    </div>
  );
};

export default Get_stock_chart;