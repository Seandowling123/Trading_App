import React, { useState, useEffect } from 'react';
import axios from 'axios';
import StockChart from './Plot_data.js';
import AccountDetails from './account_details.js';

function Get_stock_chart() {
  const [historical_data, setHistorical_data] = useState('');
  const [trade_history, setTrade_history] = useState('');
  const [account_details, setAccount_details] = useState('');

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/api/historical_data/SPY')
    //axios.get('http://51.20.79.10:8000/api/historical_data/SPY')
      .then(response => {
        setHistorical_data(response.data.financial_data);
      })
      .catch(error => {
        console.log(error);
      });
  }, []);

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/api/trade_history')
    //axios.get('http://51.20.79.10:8000/api/trade_history')
      .then(response => {
        setTrade_history(response.data.trade_history);
      })
      .catch(error => {
        console.log(error);
      });
  }, []);

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/api/account_details')
    //axios.get('http://51.20.79.10:8000/api/account_details')
      .then(response => {
        setAccount_details(response.data.account_details);
      })
      .catch(error => {
        console.log(error);
      });
  }, []);
  
  
  //console.log(historical_data);
  //console.log(trade_history);
  console.log(account_details);

  return (
    <div id="page-container">
      <StockChart historical_data={historical_data} markersData={trade_history}/>
      <AccountDetails account_details={account_details}/>
    </div>
  );
}

export default Get_stock_chart;