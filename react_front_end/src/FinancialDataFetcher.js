import React, { useState, useEffect } from 'react';
import axios from 'axios';
import StockChart from './Plot_data.js';

function HelloWorld() {
  const [message, setMessage] = useState('');

  useEffect(() => {
    axios.get('http://localhost:8000/api/hello-world/')
      .then(response => {
        setMessage(response.data.message);
      })
      .catch(error => {
        console.log(error);
      });
  }, []);

  return (
    <div>
      <h1>{message}</h1>
      <p>{message}</p>
    </div>
  );
}

function Get_financial_data() {
  const [message, setMessage] = useState('');

  useEffect(() => {
    axios.get('http://localhost:8000/api/historical_data/AAPL/week')
      .then(response => {
        setMessage(response.data.message);
        console.log(message);
      })
      .catch(error => {
        console.log(error);
      });
  }, []);

  return (
    <div>
      <h1>Historical Stock Chart</h1>
      <StockChart data={message} />
    </div>
  );
}

export default Get_financial_data;
//export default HelloWorld;
// <StockChart data={message} />