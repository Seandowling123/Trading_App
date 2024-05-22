import React from 'react';

const AccountDetails = ({ account_details }) => {
    // Calculate profit/loss
    const profit_loss = (parseFloat(account_details.portfolio_value) - parseFloat(account_details.start_balance)).toFixed(2);
  
    // Format currency
    const formattedPortfolioValue = parseFloat(account_details.portfolio_value).toLocaleString('en-US', {
      style: 'currency',
      currency: 'USD',
    });

    const formattedProfitLoss = parseFloat(profit_loss).toLocaleString('en-US', {
        style: 'currency',
        currency: 'USD',
      });
  
    // Add plus sign if profit_loss is positive
    const formattedProfitLossWithSign = profit_loss >= 0 ? `+${formattedProfitLoss}` : `-${formattedProfitLoss}`;
  
    return (
      <div id="account-detail-container">
        <h2>Portfolio Summary</h2>
        <p><strong>Balance:</strong> {formattedPortfolioValue}</p>
        <p><strong>Total P/L:</strong> {formattedProfitLossWithSign}</p>
        <p><strong>Position:</strong> {account_details.current_position}</p>
      </div>
    );
};

export default AccountDetails;