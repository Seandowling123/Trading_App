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
      <Get_stock_chart />
      
    </div>
  );
}

export default App;
