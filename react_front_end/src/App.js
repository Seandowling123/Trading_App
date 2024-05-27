import logo from './logo.svg';
import './App.css';
import React from 'react';
import Get_stock_chart from './FinancialDataFetcher';
import PopupButton from './popup_button';

// react_front_end directory
// npm start
// npm run build

function App() {
  return (
    <div id="page-container">
      <div id="title">
        <h1>Trading Activity</h1>
      </div>
      < Get_stock_chart />
    </div>
  );
}

export default App;
