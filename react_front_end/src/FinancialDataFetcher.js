import React, { useState, useEffect } from 'react';
import axios from 'axios';
import StockChart from './Plot_data.js';

function Get_stock_chart() {
  const [message, setMessage] = useState('');

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/api/historical_data/SPY')
    //axios.get('http://51.20.79.10:8000/api/historical_data/SPY')
      .then(response => {
        setMessage(response.data.financial_data);
        console.log('here');
        console.log(message);
      })
      .catch(error => {
        console.log(error);
      });
  }, []);

  return (
    <div>
      <h1>Historical Stock Chart</h1>
      <StockChart data={message}/>
    </div>
  );
}

export default Get_stock_chart;
//export default HelloWorld;
// <StockChart data={message} />