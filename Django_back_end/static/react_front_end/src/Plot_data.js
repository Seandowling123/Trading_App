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
    };
    const upper_trace = {
      x: dateObjects,
      y: data['Upper Band'],
      type: 'scatter',
      mode: 'lines',
      line: { color: '#FFC06B', width: 1.5 },
      fill: 'tonexty',
      fillcolor: 'rgba(255, 192, 107, 0.05)'
    };
    const lower_trace = {
      x: dateObjects,
      y: data['Lower Band'],
      type: 'scatter',
      mode: 'lines',
      line: { color: '#FFC06B', width: 1.5 },
      fill: 'tonexty',
      fillcolor: 'rgba(255, 192, 107, 0.3)'
    };
  
    // Array containing all trace objects
    const traces = [close_trace, upper_trace, lower_trace];

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
