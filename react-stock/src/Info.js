import React from 'react';
import './Info.css';

function Title() {
  return <div className="info-box">
    Information
    <br />
    Enter in the ticker symbol of the stock to analyse in the input box, and click on the “make predictions” button. The machine learning python model I’ve created will forecast whether the stock will increase in price over the next day, next week, and next month. This prediction is based on rolling averages/other metrics of different sectors, metrics of the general market, and past data of the stock that is being analysed. With the use of backtracking (checking how the algorithm performs on past data), we are also able to see the precision of the algorithm’s outputted predictions. 
    <br />
    Note: It may take up to 10 seconds to see the result.

  </div>;
}

export default Title;
