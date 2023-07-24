import React, { useState } from 'react';
import axios from 'axios';
import './style.css';

function StringInput() {
  const [inputValue, setInputValue] = useState('');
  const [outputValue, setOutputValue] = useState(null); // Set initial value to null

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

      setOutputValue(response.data); // Use response.data directly
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="container">
      <h2>Input the stock ticker as a string</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={inputValue}
          onChange={handleChange}
          placeholder="Enter a ticker symbol"
        />
        <button type="submit">Submit</button>
      </form>
      {outputValue && (
        <div className="output-container">
          <p>Day Precision: {outputValue.day_precision}</p>
          <p>Week Precision: {outputValue.week_precision}</p>
        </div>
      )}
    </div>
  );
}

export default StringInput;
