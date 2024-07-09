import logo from './logo.svg';
import './App.css';
import React from 'react';
import Get_stock_chart from './FinancialDataFetcher';

// react_front_end directory
// npm start
// npm run build

function App() {
  return (
    <div id="page-container">
      <div id="title">
        <h1>Daily Trading Activity</h1>
      </div>
      <div id="notice"><p>Real time algorithmic trading information for the ticker SPY. Note that the algorithm currently operates on a paper trading account with a high balance for compliance with trading regulations.</p></div>
      < Get_stock_chart />
    </div>
  );
}

export default App;
