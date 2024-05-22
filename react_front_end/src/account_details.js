import React from 'react';

const AccountDetails = ({ account_details }) => {

    const profit_loss = (parseFloat(account_details.portfolio_value) - parseFloat(account_details.start_balance)).toFixed(2);

    return (
        <div id="account-detail-container">
            <h2>Portfolio Summary</h2>
            <p>Balance: &nbsp;&nbsp;${account_details.portfolio_value}</p>
            <p>Total P/L: &nbsp;${profit_loss}</p>
            <p>Position: &nbsp;&nbsp;{account_details.current_position}</p>
        </div>
        );
};

export default AccountDetails;