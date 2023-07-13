import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# For Machine Learning:
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score

import yfinance as yf

# from flask import Flask, render_template
# app = Flask(__name__)
# @app.route('/stocks')
# def home():

def predict(train, test, predictors, DayModel):
    DayModel.fit(train[predictors], train["1DayIncrease"])
    predsDay = DayModel.predict(test[predictors])
    predsDay = pd.Series(predsDay, index=test.index, name="Predictions")
    combined = pd.concat([test["1DayIncrease"], predsDay], axis=1)
    return combined

def backtest(data, model, predictors, start=2500, step=250):
    all_predictions = []

    for i in range(start, data.shape[0], step):
        train = data.iloc[0:i].copy()
        test = data.iloc[i:(i+step)].copy()
        predictions = predict(train, test, predictors, model)
        all_predictions.append(predictions)
    
    return pd.concat(all_predictions)

def main():
    # Define the ticker symbol for the stock/fund to look at
    # S&P
    # ticker_symbol = '^GSPC'
    ticker_symbol = 'VFV.TO'

    # Retrieve historical price data using yfinance
    data = yf.download(ticker_symbol, start='2000-01-01')
    # metrics_df = pd.DataFrame(columns=['Ticker', 'P/E Ratio', 'P/B Ratio'])
    # Create an empty DataFrame to store the metrics
    metrics_df = pd.DataFrame(columns=['Ticker', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume'])

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

    # plt.plot(data.index, data['Close'])

    # Close price of the following day  (for backtesting)
    metrics_df['Tomorrow'] = metrics_df['Close'].shift(-1)

    #to determine if tomorrow's price (close) is greater than todays(close), (for backtesting)
    metrics_df['1DayIncrease'] = metrics_df['Tomorrow'] > metrics_df['Close']

    # Close price for the following week (5 business days away)
    metrics_df['NextWeek'] = metrics_df['Close'].shift(-5)

    #to determine if it will go up over the next week
    metrics_df['1WeekIncrease'] = metrics_df['NextWeek'] > metrics_df['Close']

    #machine learning with sklearn
    #model

    DayModel = RandomForestClassifier(n_estimators=100, min_samples_split=100, random_state=1)
    WeekModel = RandomForestClassifier(n_estimators=100, min_samples_split=100, random_state=1)

    # train = metrics_df.iloc[:-100]
    # test = metrics_df.iloc[-100:]

    predictors = ["Close", "Volume", "Open", "High", "Low"]

    #Back test the model
    predictions = backtest(metrics_df, DayModel, predictors)
    #Predictions was added in to the metrics_df table, now use count to analyse
    predictions["Predictions"].value_counts()
    # DayPrediction = predict(train, test, predictors, DayModel)
    precision = precision_score(predictions["1DayIncrease"], predictions["Predictions"])

    print(precision)

if __name__ == "__main__":
    main()
    # DayModel.fit(train[predictors], train["1DayIncrease"])
    # WeekModel.fit(train[predictors], train["1WeekIncrease"])

    # # Generate predictions and turn them in to a pandas series instead of a numpy array
    # predsDay = DayModel.predict(test[predictors])
    # predsWeek = WeekModel.predict(test[predictors])
    # predsDay = pd.Series(predsDay, index=test.index)
    # predsWeek = pd.Series(predsWeek, index=test.index)

    # scoreDay = precision_score(test["1DayIncrease"], predsDay)
    # scoreWeek = precision_score(test["1WeekIncrease"], predsWeek)
    # # print(score)
    # x = {'stock_data': scoreDay}
    # y = {'stock_data': scoreWeek}

    # #use pandas library to round entire table to two decimals
    # metrics_df = metrics_df.round(2)

    # print('here are the precison scores for day and week')
    # print(x)
    # print(y)

    #return render_template('index.html', stock_data=metrics_df)
    # return render_template('index2.html', x=x)

    # if __name__ == '__main__':
    #     app.run(debug=True)

