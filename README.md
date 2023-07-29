# Machine Learning Stock Predictor Web Application

## Demo and Code Walk-Through: 
https://youtu.be/IHdjdF6lIEg

## Overview
Flask web app with Python and Sklearn backend model that uses metrics of the specified stock, different sectors, and overall market over the past 20 years to predict whether a stock will increase over the next day and week. The Frontend is built in React and allows a user to input a stock ticker, and have the predictions output to the screen. The precision of these predictions is also output to the screen as it is found through backtesting when the user inputs the stock.

### Check list
- [x] Find somewhere to ~scrape~ access data from 
- [x] Determine which stocks to take in based on market cap and long term stability
- [x] Decide which metrics to take in for each stock
- [x] Create simple html file and connect to python with flask
- [x] Use machine learning to make stock price predictions
- [x] Back Test the algorithm
- [x] Add in sectors going up or down over the same time period ( and see if precision improves )
- [x] Add in other sector info that improves precision
- [x] Tech sector
- [x] Energy sector
- [x] Financials sector
- [x] Industrial sector
- [x] Real Estate sector
- [x] Create simple html frontend to verify flask app is working as expected
- [x] Create simple React front end
- [x] Connect React to Python
- [x] Send all necessary information from Flask to React frontend. App is working as expected at this point
- [x] Make the frontend presentable
- [ ] Host the application
- [x] Add error handling message
- [ ] Add Video Demo
