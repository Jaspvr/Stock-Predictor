import pandas as pd
import matplotlib.pyplot as plt
import requests
from datetime import datetime

# For Machine Learning:
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score
from sklearn.experimental import enable_hist_gradient_boosting 
from sklearn.ensemble import HistGradientBoostingClassifier

import yfinance as yf


from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app, resources={r"/stocks": {"origins": "*"}})

def is_valid_ticker_symbol(symbol):
    try:
        # Check if the stock exists in Yahoo Finance
        stock = yf.Ticker(symbol)
        return True
    except:
        return False

def predictDay(train, test, predictors, DayModel):
    DayModel.fit(train[predictors], train["1DayIncrease"])
    predsDay = DayModel.predict(test[predictors])
    predsDay = pd.Series(predsDay, index=test.index, name="Predictions")
    combined = pd.concat([test["1DayIncrease"], predsDay], axis=1)
    return combined

def backtestDay(data, model, predictors, start=2500, step=250):
    all_predictions = []

    for i in range(start, data.shape[0], step):
        train = data.iloc[0:i].copy()
        test = data.iloc[i:(i+step)].copy()
        predictions = predictDay(train, test, predictors, model)
        all_predictions.append(predictions)
    
    return pd.concat(all_predictions)

def predictWeek(train, test, predictors, WeekModel):
    WeekModel.fit(train[predictors], train["1WeekIncrease"])
    predsDay = WeekModel.predict(test[predictors])
    predsDay = pd.Series(predsDay, index=test.index, name="Predictions")
    combined = pd.concat([test["1WeekIncrease"], predsDay], axis=1)
    return combined

def backtestWeek(data, model, predictors, start=2500, step=250):
    all_predictions = []

    for i in range(start, data.shape[0], step):
        train = data.iloc[0:i].copy()
        test = data.iloc[i:(i+step)].copy()
        predictions = predictWeek(train, test, predictors, model)
        all_predictions.append(predictions)
    
    return pd.concat(all_predictions)

def outputtedPredictDay(train, test, predictors, DayModel):
    DayModel.fit(train[predictors], train["1DayIncrease"])
    predsDay = DayModel.predict(test[predictors])
    return predsDay


@app.route('/stocks', methods=['GET'])
def home():
    # Define the ticker symbol for the stock/fund to look at
    # S&P
    # ticker_symbol = '^GSPC'
    # ticker_symbol = 'VFV.TO'
    ticker_symbol = request.args.get('ticker_symbol')

    if not ticker_symbol or not is_valid_ticker_symbol(ticker_symbol):
        error_message = "Invalid stock ticker symbol."
        return jsonify({"error": error_message})

    # To represent how sectors are doing (we will just look at the price)
    tech_symbol = 'XLK'
    energy_symbol = 'XLE'
    financial_symbol = 'XLF'
    industrial_symbol = 'XLI'
    real_estate_symbol = 'VNQ'

    # Retrieve historical price data of the stock and sectors we are analysing using yfinance
    start_of_data = '2000-01-01'
    data = yf.download(ticker_symbol, start_of_data)
    tech_data = yf.download(tech_symbol, start_of_data)
    energy_data = yf.download(energy_symbol, start_of_data)
    financial_data = yf.download(financial_symbol, start_of_data)
    industrial_data = yf.download(industrial_symbol, start_of_data)
    real_estate_data = yf.download(real_estate_symbol, start_of_data)

    # Create an empty DataFrame to store the metrics
    metrics_df = pd.DataFrame(columns=['Ticker', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
    # Same but for the sectors
    tech_metrics_df = pd.DataFrame(columns=['Ticker', 'Open', 'Close', 'Volume'])
    energy_metrics_df = pd.DataFrame(columns=['Open', 'Close', 'Volume'])
    financial_metrics_df = pd.DataFrame(columns=['Open', 'Close', 'Volume'])
    industrial_metrics_df = pd.DataFrame(columns=['Open', 'Close', 'Volume'])
    real_estate_metrics_df = pd.DataFrame(columns=['Open', 'Close', 'Volume'])

    # Populate the metrics DataFrame with historical price data
    metrics_df = pd.concat([metrics_df, pd.DataFrame({
        'Ticker': [ticker_symbol] * len(data),
        'Date': data.index,
        'Open': data['Open'].values,
        'High': data['High'].values,
        'Low': data['Low'].values,
        'Close': data['Close'].values,
        'Volume': data['Volume'].values
    })])

    tech_metrics_df = pd.concat([tech_metrics_df, pd.DataFrame({
        'Ticker': [ticker_symbol]*len(tech_data), 
        'Open': tech_data['Open'].values,
        'Close': tech_data['Close'].values,
        'Volume': tech_data['Volume'].values
    })])

    energy_metrics_df = pd.concat([energy_metrics_df, pd.DataFrame({
        'Open': energy_data['Open'].values,
        'Close': energy_data['Close'].values,
        'Volume': energy_data['Volume'].values
    })])

    financial_metrics_df = pd.concat([financial_metrics_df, pd.DataFrame({
        'Open': financial_data['Open'].values,
        'Close': financial_data['Close'].values,
        'Volume': financial_data['Volume'].values
    })])

    industrial_metrics_df = pd.concat([industrial_metrics_df, pd.DataFrame({
        'Open': industrial_data['Open'].values,
        'Close': industrial_data['Close'].values,
        'Volume': industrial_data['Volume'].values
    })])

    real_estate_metrics_df = pd.concat([real_estate_metrics_df, pd.DataFrame({
        'Open': real_estate_data['Open'].values,
        'Close': real_estate_data['Close'].values,
        'Volume': real_estate_data['Volume'].values
    })])

    # Close price of the following day  (for backtesting)
    metrics_df['Tomorrow'] = metrics_df['Close'].shift(-1)
    # Prices for sectors
    tech_metrics_df['NextWeek'] = tech_metrics_df['Close'].shift(-5)
    energy_metrics_df['NextWeek'] = energy_metrics_df['Close'].shift(-5)
    financial_metrics_df['NextWeek'] = financial_metrics_df['Close'].shift(-5)
    financial_metrics_df['TwoWeek'] = financial_metrics_df['Close'].shift(-10)
    industrial_metrics_df['NextWeek'] = industrial_metrics_df['Close'].shift(-5)
    real_estate_metrics_df['NextWeek'] = industrial_metrics_df['Close'].shift(-5)

    #to determine if tomorrow's price (close) is greater than todays(close), (for backtesting)
    metrics_df['1DayIncrease'] = metrics_df['Tomorrow'] > metrics_df['Close']
    #add in sector columns
    metrics_df['TechIncreaseWeek'] = tech_metrics_df['NextWeek'] > tech_metrics_df['Close']
    metrics_df['TechVolume'] = tech_metrics_df['Volume']
    metrics_df['EnergyIncreaseWeek'] = energy_metrics_df['NextWeek'] > energy_metrics_df['Close']
    metrics_df['EnergyVolume'] = energy_metrics_df['Volume']
    metrics_df['FinancialIncreaseWeek'] = financial_metrics_df['NextWeek'] > financial_metrics_df['Close']
    metrics_df['FinancialVolume'] = financial_metrics_df['Volume']
    metrics_df['IndustrialIncreaseWeek'] = industrial_metrics_df['NextWeek'] > industrial_metrics_df['Close']
    metrics_df['IndustrialVolume'] = industrial_metrics_df['Volume']
    metrics_df['RealEstateIncreaseWeek'] = real_estate_metrics_df['NextWeek'] > real_estate_metrics_df['Close']
    metrics_df['RealEstateVolume'] = real_estate_metrics_df['Volume']

    # Close price for the following week (5 business days away)
    metrics_df['NextWeek'] = metrics_df['Close'].shift(-5)

    #to determine if it will go up over the next week
    metrics_df['1WeekIncrease'] = metrics_df['NextWeek'] > metrics_df['Close']

    #machine learning with sklearn
    #model
    DayModel = HistGradientBoostingClassifier(max_iter=200, learning_rate=0.1, random_state=1)
    WeekModel = HistGradientBoostingClassifier(max_iter=200, learning_rate=0.1, random_state=1)

    predictors = ["Close", "Volume", "Open", "High", "Low", "TechIncreaseWeek", "TechVolume", "EnergyIncreaseWeek", "EnergyVolume", "FinancialIncreaseWeek", "FinancialVolume", "IndustrialVolume", "RealEstateVolume"]

    #Back test the models
    DayPredictions = backtestDay(metrics_df, DayModel, predictors)
    WeekPredictions = backtestWeek(metrics_df, WeekModel, predictors)

    #Predictions was added in to the metrics_df table, now use count to analyse
    DayPredictions["Predictions"].value_counts()
    WeekPredictions["Predictions"].value_counts()

    # DayPrediction = predict(train, test, predictors, DayModel)
    DayPrecision = precision_score(DayPredictions["1DayIncrease"], DayPredictions["Predictions"])
    WeekPrecision = precision_score(WeekPredictions["1WeekIncrease"], WeekPredictions["Predictions"])

    # Prepare the data to pass to the template
    DayPrecision = str(DayPrecision)
    WeekPrecision = str(WeekPrecision)


    #Make predictions based on the models

    # 1 Day Prediction
    # Remove tomorrow's data from test dataset to ensure no error occurs (tomorrow's price doesn't exist yet), and set data to most current data
    tomorrow_test_data = metrics_df.iloc[-1][predictors].values.reshape(1, -1)
    tomorrow_price_prediction = DayModel.predict(tomorrow_test_data)
    
    next_week_test_data = metrics_df.iloc[-5][predictors].values.reshape(1, -1)
    next_week_price_prediction = WeekModel.predict(next_week_test_data)
    
    #Prediction messages to client
    prediction_message_day = ""
    if tomorrow_price_prediction == True:
        prediction_message_day = "The stock will likely go up in one trading day."
    else:
        prediction_message_day = "The stock will likely not go up in one trading day."

    prediction_message_week = ""
    if next_week_price_prediction == True:
        prediction_message_week = "The stock will likely go up in one week (5 trading days)."
    else:
        prediction_message_week = "The stock will likely not go up in one week (5 trading days)."

    # Prepare the data to pass to the template
    DayPrecision = str(DayPrecision)
    WeekPrecision = str(WeekPrecision)

    context = {
        'day_precision': DayPrecision,
        'week_precision': WeekPrecision,
        'prediction_message_day': prediction_message_day,
        'prediction_message_week': prediction_message_week,
    }

    return jsonify(context)

if __name__ == "__main__":
    app.run()
