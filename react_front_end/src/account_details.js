import React from 'react';

const AccountDetails = ({ account_details }) => {

    return (
        <div id="account-detail-container">
            <h2>Portfolio Summary</h2>
            <p>{account_details.portfolio_value}</p>
        </div>
        );
};

export default AccountDetails;