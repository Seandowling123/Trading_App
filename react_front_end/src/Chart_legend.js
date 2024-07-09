import React from 'react';

const ChartLegend = () => {
    return (
        <div className="chart-descriptions">
            <h3>Legend</h3>
            <div className="description-item">
                <div className="color-box-filled" style={{ backgroundColor: '#007bff', width: '25px', height: '5px', marginRight: '10px' }}></div>
                <div className="description-text">Close Price</div>
            </div>
            <div className="description-item">
                <div className="color-box-filled" style={{ backgroundColor: '#FFC06B', width: '25px', height: '5px', marginRight: '10px' }}></div>
                <div className="description-text">Bollinger Bands</div>
            </div>
            <div className="description-item">
                <div className="color-box green"></div>
                <div className="description-text">Buy Trade Executed</div>
            </div>
            <div className="description-item">
                <div className="color-box red"></div>
                <div className="description-text">Sell Trade Executed</div>
            </div>
            <p>Click on a trade for detailed information.</p>
        </div>
    );
};

export default ChartLegend;