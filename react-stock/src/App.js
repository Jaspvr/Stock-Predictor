import React from 'react';
import StringInput from './StringInput';
import TitleBox from './Title';
import InfoBox from './Info';
import './App.css';

function App() {
  return (
    <div className="app-container">
    <div className="component-container">
      <TitleBox />
      <InfoBox />
    </div>
    <div className="string-input-container">
      <StringInput />
    </div>
  </div>
  );
}

export default App;
