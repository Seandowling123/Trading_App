import React, { useState, useEffect } from 'react';
import axios from 'axios';
import StockChart from './Plot_data.js';

function Get_stock_chart() {
  const [historical_data, setHistorical_data] = useState('');
  const [trade_history, setTrade_history] = useState('');

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/api/historical_data/SPY')
    //axios.get('http://51.20.79.10:8000/api/historical_data/SPY')
      .then(response => {
        setHistorical_data(response.data.financial_data);
        //console.log(historical_data);
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
        console.log(trade_history);
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
        console.log(trade_history);
      })
      .catch(error => {
        console.log(error);
      });
  }, []);

  return (
    <div>
      <h1>Trading Activity</h1>
      <StockChart historical_data={historical_data} markersData={trade_history}/>
    </div>
  );
}

export default Get_stock_chart;
//export default HelloWorld;
// <StockChart data={historical_data} />