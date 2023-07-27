import React from 'react';
import StringInput from './StringInput';
import TitleBox from './Title';
import InfoBox from './Info';
import './App.css';

function App() {
  return (
    <div className = "component-container">
      <TitleBox />
      <InfoBox />
      <StringInput />
    </div>
  );
}

export default App;
