import React, { useState } from 'react';

function PopupButton() {
  const [isPopupOpen, setIsPopupOpen] = useState(false);

  const togglePopup = () => {
    setIsPopupOpen(!isPopupOpen);
  };

  return (
    <div>
      <button style={buttonStyles} onClick={togglePopup}>Click me</button>
      {isPopupOpen && (
        <div style={popupStyles}>
          <div style={popupInnerStyles}>
            <h1>I love you &lt;3</h1>
            <button onClick={togglePopup}>Close</button>
          </div>
        </div>
      )}
    </div>
  );
}

const buttonStyles = {
    backgroundColor: '#121212', // Bootstrap primary color
    //backgroundColor: 'red',
    color: '#121212', // White text color
    fontWeight: 'bold',
    border: 'none', // Remove default border
    padding: '10px 20px', // Add padding
    fontSize: '16px', // Increase font size
    borderRadius: '5px', // Rounded corners
    cursor: 'pointer', // Pointer cursor on hover
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)', // Subtle shadow for depth
    transition: 'background-color 0.3s ease', // Smooth transition for background color
    height: '130px',
    width: '130px',
  };

const popupStyles = {
  position: 'fixed',
  top: 0,
  left: 0,
  width: '100%',
  height: '100%',
  backgroundColor: 'rgba(0, 0, 0, 0.5)',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  zIndex: 1000,
};

const popupInnerStyles = {
  backgroundColor: 'white',
  padding: '20px',
  borderRadius: '10px',
  textAlign: 'center',
  color: 'black',
  zIndex: 1001,
};

export default PopupButton;
