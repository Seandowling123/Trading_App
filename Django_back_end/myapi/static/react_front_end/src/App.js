import logo from './logo.svg';
import './App.css';
import React from 'react';
import Get_stock_chart from './FinancialDataFetcher';

// Django_back_end/myapi/static/react_front_end directory
// npm start

function App() {
  return (
    <div id="plot-container">
      <Get_stock_chart />
    </div>
  );
}

export default App;
