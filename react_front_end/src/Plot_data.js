import React, { useState } from 'react';
import Plot from 'react-plotly.js';

// MarkerDetails component to display marker information
const MarkerDetails = ({ marker }) => (
  <div>
    <h3>Trade Details</h3>
    <p>{marker.side}</p>
    <p>${marker.filled_avg_price}</p>
    <p>{Date(marker.datetime)}</p>
  </div>
);

const StockChart = ({ historical_data, markersData }) => {

    const [clickedMarker, setClickedMarker] = useState(null);

    if (!historical_data || historical_data.length === 0) {
      return <div>Loading Trading Data.</div>;
    }

    // Convert strings to Date objects
    const dateObjects = historical_data['Datetime'].map(dateString => new Date(dateString));
  
    const close_trace = {
      x: dateObjects,
      y: historical_data['Close'],
      type: 'scatter',
      mode: 'lines',
      line: { color: '#007bff', width: 2 },
      name: 'Close Price'
    };
    const upper_trace = {
      x: dateObjects,
      y: historical_data['Lower Band'],
      type: 'scatter',
      mode: 'lines',
      line: { color: '#FFC06B', width: 1.5 },
      fill: 'tonexty',
      fillcolor: 'rgba(255, 192, 107, 0.05)',
      name: 'Lower Band'
    };
    const lower_trace = {
      x: dateObjects,
      y: historical_data['Upper Band'],
      type: 'scatter',
      mode: 'lines',
      line: { color: '#FFC06B', width: 1.5 },
      fill: 'tonexty',
      fillcolor: 'rgba(255, 192, 107, 0.3)',
      name: 'Upper Band'
    };
  
    // Array containing all trace objects
    const traces = [close_trace, upper_trace, lower_trace];

    // Convert markersData to an array of objects
    const markerArray = markersData.datetime.map((datetime, index) => ({
      datetime,
      side: markersData.side[index],
      filled_avg_price: markersData.filled_avg_price[index]
    }));

    // Add shapes for buy and sell points
    const shapes = markerArray.map((trade) => ({
      type: 'line',
      xref: 'x',
      yref: 'paper',
      x0: new Date(trade.datetime),
      x1: new Date(trade.datetime),
      y0: 0,
      y1: 1,
      line: {
        color: trade.side === 'buy' ? 'green' : 'red', // Green for buy, red for sell
        width: 2,
        dash: 'dot'
      },
      name: trade.side === 'buy' ? 'Buy Point' : 'Sell Point'
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

    // Handle click events
    const handleClick = (event) => {
      if (event.points) {
        event.points.forEach(point => {
          const clickedMarker = markerArray.find(marker => new Date(marker.datetime).getTime() === new Date(point.x).getTime());
          if (clickedMarker) {
            setClickedMarker(clickedMarker); // Update state with clicked marker
          }
        });
      }
    };
  
    return (
      <div id="trade-info-container">
        <div id="#plot-container">
          <Plot
            data={traces}
            layout={layout}
            style={{ width: '900px', height: '600px' }}
            onClick={handleClick}
          />
        </div>
        <div id="trade-marker">
          {clickedMarker && <MarkerDetails marker={clickedMarker} />} {/* Render MarkerDetails if a marker is clicked */}
        </div>
      </div>
    );
  };

export default StockChart;
