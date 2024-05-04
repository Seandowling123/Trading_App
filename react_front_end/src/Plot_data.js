import React from 'react';
import Plot from 'react-plotly.js';

const StockChart = ({ data }) => {
  if (!data || data.length === 0) {
    return <div>No data available</div>;
  }

  const trace = {
    x: data['Date'],
    y: data['Adj Close'],
    type: 'scatter',
    mode: 'lines',
    line: { color: 'blue' }
  };

  const layout = {
    title: 'Historical Stock Prices',
    xaxis: {
      title: 'Date'
    },
    yaxis: {
      title: 'Close Price'
    }
  };

  return (
    <Plot
      data={[trace]}
      layout={layout}
      style={{ width: '100%', height: '400px' }}
    />
  );
};

export default StockChart;
