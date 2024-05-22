import React from 'react';
import Plot from 'react-plotly.js';

const StockChart = ({ data }) => {
    if (!data || data.length === 0) {
      return <div>No data available</div>;
    }

    // Convert strings to Date objects
    const dateObjects = data['Datetime'].map(dateString => new Date(dateString));
  
    const close_trace = {
      x: dateObjects,
      y: data['Close'],
      type: 'scatter',
      mode: 'lines',
      line: { color: '#007bff', width: 2 },
      name: 'Close Price'
    };
    const upper_trace = {
      x: dateObjects,
      y: data['Lower Band'],
      type: 'scatter',
      mode: 'lines',
      line: { color: '#FFC06B', width: 1.5 },
      fill: 'tonexty',
      fillcolor: 'rgba(255, 192, 107, 0.05)',
      name: 'Lower Band'
    };
    const lower_trace = {
      x: dateObjects,
      y: data['Upper Band'],
      type: 'scatter',
      mode: 'lines',
      line: { color: '#FFC06B', width: 1.5 },
      fill: 'tonexty',
      fillcolor: 'rgba(255, 192, 107, 0.3)',
      name: 'Upper Band'
    };
  
    // Array containing all trace objects
    const traces = [close_trace, upper_trace, lower_trace];

    // Buy + sell markers
    const ex_buy_date_string = ["2024-05-21T13:11:00-04:00"];
    const ex_buy_date = ex_buy_date_string.map(dateString => new Date(dateString));
    console.log(ex_buy_date)

    // Add shapes for buy and sell points
    const shapes = ex_buy_date.map((date) => ({
      type: 'line',
      xref: 'x',
      yref: 'paper',
      x0: date.date,
      x1: date.date,
      y0: 0,
      y1: 1,
      line: {
        //color: date.type === 'buy' ? 'green' : 'red', // Green for buy, red for sell
        color: 'green',
        width: 2,
        dash: 'dot'
      },
      name: date.type === 'buy' ? 'Buy Point' : 'Sell Point'
    }));

    const layout = {
      xaxis: {
        tickfont: { size: 14, family: 'Arial, sans-serif', color: '#777' }, // Larger tick font size and custom font family
        gridcolor: '#f0f0f0', // Light gray gridlines
        gridwidth: 1, // Gridline width
        showspikes: true, // Show spikes on hover
        spikemode: 'across', // Show spikes across all traces
        spikedash: 'solid',
        spikecolor: '#d3d3d3',
        spikethickness: 1, // Spike thickness
        spikesnap: 'data', // Snap to cursor position
      },
      yaxis: {
        tickfont: { size: 14, family: 'Arial, sans-serif', color: '#777' }, // Larger tick font size and custom font family
        gridcolor: '#f0f0f0', // Light gray gridlines
        gridwidth: 1, // Gridline width
        showspikes: true, // Show spikes on hover
        spikemode: 'across', // Show spikes to axis
        spikedash: 'solid',
        spikecolor: '#d3d3d3',
        spikethickness: 2, // Increase spike thickness for solid line
        spikesnap: 'data', 
      },
      shapes: shapes, // Add shapes for buy and sell points
      showlegend: false, // Hide the legend
      hovermode: 'x unified', // Show hover information for all traces at the same x-axis value
      plot_bgcolor: '#fff', // White background color
      paper_bgcolor: '#fff', // White paper background color
      autosize: true, // Automatically adjust size based on container
    };
  
    return (
      <Plot
        data={traces}
        layout={layout}
        style={{ width: '100%', height: '600px' }} // Increase height for better visualization
      />
    );
  };

export default StockChart;
