import React, { useState } from 'react';
import axios from 'axios';
import './style.css';

function StringInput() {
  const [inputValue, setInputValue] = useState('');
  const [outputValue, setOutputValue] = useState(null);
  const [errorMessage, setErrorMessage] = useState('');

  const handleChange = (event) => {
    setInputValue(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const response = await axios.get('http://127.0.0.1:5000/stocks', {
        params: {
          ticker_symbol: inputValue,
        },
      });

      // Error handling
      if (response.data.error) {
        setErrorMessage(response.data.error);
        setOutputValue(null); 
      } else {
        setOutputValue(response.data);
        setErrorMessage(''); // clear any previous error messages
      }
 
    } catch (error) {
      console.error(error);
      setErrorMessage('An error occurred while fetching data. Please check that you entered a valid stock ticker symbol.');
    }
  };

  return (
    <div className="container">
      <div className="input-container">
        <input
          className="input-box"
          type="text"
          value={inputValue}
          onChange={handleChange}
          placeholder="Enter a ticker symbol"
        />
      </div>
      <div className="button-container">
        <button className="submit-button" type="submit" onClick={handleSubmit}>
          Make Predictions
        </button>
      </div>
      {errorMessage && <p className="error-message">{errorMessage}</p>}
      {outputValue && !errorMessage && (
        <div className="output-container">
          <p>Day Prediction: {outputValue.prediction_message_day}</p>
          <p>Week Prediction: {outputValue.prediction_message_week}</p>
          <p>Day Precision: {outputValue.day_precision}</p>
          <p>Week Precision: {outputValue.week_precision}</p>
        </div>
      )}
    </div>
  );
}

export default StringInput;
