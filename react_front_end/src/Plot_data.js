import React, { useState } from 'react';
import Plot from 'react-plotly.js';

// Function to get today's date formatted
const getFormattedDate = ( start_date ) => {
  const options = { year: 'numeric', month: 'long', day: 'numeric' };
  return start_date.toLocaleDateString('en-US', options);
};

// MarkerDetails component to display marker information
const MarkerDetails = ({ marker }) => {
  // Format date
  const formattedDate = new Date(marker.datetime).toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: 'numeric',
    minute: 'numeric',
    hour12: false
  });

  // Format currency
  const formattedPrice = parseFloat(marker.filled_avg_price).toLocaleString('en-US', {
    style: 'currency',
    currency: 'USD',
  });

  return (
    <div className="marker-details">
      <h3>Trade Details - {marker.side === 'buy' ? 'Buy' : 'Sold'} - {marker.symbol}</h3>
      <p><strong>Price:</strong> {formattedPrice}</p>
      <p><strong>Date:</strong> {formattedDate}</p>
    </div>
  );
};

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
    let markerArray = []

    // Convert markersData to an array of objects
    if (markersData.length !== 0) {
      markerArray = markersData.datetime.map((datetime, index) => ({
        datetime,
        side: markersData.side[index],
        symbol: markersData.symbol[index],
        filled_avg_price: markersData.filled_avg_price[index],
      }));
    }

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
        color: trade.side === 'buy' ? '#00FF30' : '#FF0000',
        width: 3,
        dash: 'dot'
      },
      name: trade.side === 'buy' ? 'Buy Point' : 'Sell Point'
    }));

    // Determine the date range for the plot
    const startDate = new Date(dateObjects[0]);
    const endDate = new Date(startDate[dateObjects.length]);
    endDate.setDate(startDate.getDate() + 1);

    const layout = {
      title: {
        text:`SPY - ${getFormattedDate(startDate)}`,
        font: {
          family: 'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
          size: 24,
          color: 'white',
          weight: 'bold'
        },
        xref: 'paper',
      },
      xaxis: {
        tickfont: { size: 14, family: 'Arial, sans-serif', color: '#CFCFCF' }, // Larger tick font size and custom font family
        gridcolor: '#454545', // Light gray gridlines
        gridwidth: 1, // Gridline width
        showspikes: true, // Show spikes on hover
        spikemode: 'across', // Show spikes across all traces
        spikedash: 'solid',
        spikecolor: '#d3d3d3',
        spikethickness: 1, // Spike thickness
        spikesnap: 'data', // Snap to cursor position
        range: [startDate, endDate]
      },
      yaxis: {
        tickfont: { size: 14, family: 'Arial, sans-serif', color: '#CFCFCF' }, // Larger tick font size and custom font family
        gridcolor: '#454545', // Light gray gridlines
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
      plot_bgcolor: '#121212', // White background color
      paper_bgcolor: '#121212', // White paper background color
      autosize: true, // Automatically adjust size based on container
      hoverlabel: {
        font: {
          color: '#CFCFCF', // Font color
          size: 14, // Adjust font size as needed
          family: '-apple-system, BlinkMacSystemFont, sans-serif' // Font family to match the rest of the app
        },
        bgcolor: 'black', // Background color of the hover label
        bordercolor: '#CFCFCF' // Border color of the hover label
      }
    };

    // Handle click events
    const handleClick = (event) => {
      if (event.points) {
        event.points.forEach(point => {
          const clickedMarker = markerArray.find(marker => new Date(marker.datetime).getTime() === new Date(point.x).getTime());
          if (clickedMarker) {
            setClickedMarker(clickedMarker);
          }
        });
      }
    };
  
    return (
      <div id="#plot-container">
        <Plot
          data={traces}
          layout={layout}
          style={{ width: '900px', height: '500px' }}
          onClick={handleClick}
        />
        <div id="trade-marker">
          {clickedMarker && <MarkerDetails marker={clickedMarker} />} {/* Render MarkerDetails if a marker is clicked */}
        </div>
      </div>
    );
  };

export default StockChart;
