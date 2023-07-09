import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
# plt.style.use('seaborn'
# 
# 
# For Machine Learning:
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score

import yfinance as yf

# from flask import Flask, render_template

# app = Flask(__name__)

# @app.route('/stocks')
# def home():

# Define the ticker symbol for the S&P 500 index
ticker_symbol = '^GSPC'

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
metrics_df['is_increase2'] = metrics_df['NextWeek'] > metrics_df['Close']

#machine learning with sklearn
#model

model = RandomForestClassifier(n_estimators=100, min_samples_split=100, random_state=1)

train = metrics_df.iloc[:-100]
test = metrics_df.iloc[-100:]

predictors = ["Close", "Volume", "Open", "High", "Low"]
model.fit(train[predictors], train["1DayIncrease"])

preds = model.predict(test[predictors])
preds = pd.Series(preds, index=test.index)

score = precision_score(test["1DayIncrease"], preds)
# print(score)
x = {'stock_data': score}

#use pandas library to round entire table to two decimals
metrics_df = metrics_df.round(2)

print(x)

#return render_template('index.html', stock_data=metrics_df)
# return render_template('index2.html', x=x)

# if __name__ == '__main__':
#     app.run(debug=True)

# Right now this returns the data frame that we are working with with machine learning
#Instead, we want to return simply if the AI predicts if it will go up over the next day/week/month

    # #ACCESSING INDIVIDUAL STOCKS
    # aapl = yf.Ticker('aapl')
    # msft = yf.Ticker('msft')
    # amzn = yf.Ticker('amzn')
    # nvda = yf.Ticker('nvda')
    # tsla = yf.Ticker('tsla')
    # googl = yf.Ticker('googl')
    # meta = yf.Ticker('meta')
    # goog = yf.Ticker('goog')
    # brkb = yf.Ticker('brk-b')
    # unh = yf.Ticker('unh')
    # jnj = yf.Ticker('jnj')
    # jpm = yf.Ticker('jpm')
    # xom = yf.Ticker('xom')
    # v = yf.Ticker('v')
    # lly = yf.Ticker('lly')
    # pg = yf.Ticker('pg')
    # avgo = yf.Ticker('avgo')
    # ma = yf.Ticker('ma')
    # hd = yf.Ticker('hd')
    # mrk = yf.Ticker('mrk')
    # cvx = yf.Ticker('cvx')
    # pep = yf.Ticker('pep')
    # abbv = yf.Ticker('abbv')
    # cost = yf.Ticker('cost')
    # ko = yf.Ticker('ko')
    

    # # ACCESSING ALL STOCKS IN S&P
    # # sp500_tickers = yf.tickers_sp500()

    # # Store all stocks into a dictionary with their symbols as keys
    # stocks = {
    #     #1-5
    #     'aapl': aapl,
    #     'msft': msft,
    #     'amzn': amzn,
    #     'nvda': nvda,
    #     'tsla': tsla,
    #     #5-10
    #     'googl': googl,
    #     'meta': meta,
    #     'goog': goog,
    #     'brk-b': brkb, 
    #     'unh': unh,
    #     #10-15
    #     'jnj': jnj,
    #     'jpm': jpm,
    #     'xom': xom,
    #     'v': v,
    #     'lly': lly,
    #     #15-25
    #     'pg': pg,
    #     'avgo': avgo,
    #     'ma': ma,
    #     'hd': hd,
    #     'mrk': mrk,
    #     'cvx': cvx,
    #     'pep': pep,
    #     'abbv': abbv,
    #     'cost': cost,
    #     'ko': ko
    # }

    # # Create an empty dictionary to store the stock data
    # # stock_data = {}
    # metrics_df = pd.DataFrame(columns=['Ticker', 'P/E Ratio', 'P/B Ratio'])

    # # Iterate over each ticker in the S&P 500
    # for ticker in stocks:
    #     # Retrieve the stock data using the ticker symbol
    #     stock = yf.Ticker(ticker)
        
    #     # Retrieve the desired metrics
    #     pe_ratio = stock.info.get('trailingPE', 'N/A')
    #     pb_ratio = stock.info.get('priceToBook', 'N/A')
    #     current_price = yf.get_live_price(ticker)
        
    #     # Append the metrics to the DataFrame
    #     stock_df = pd.DataFrame({
    #         'Ticker': ticker,
    #         'Price': current_price,
    #         'P/E Ratio': pe_ratio,
    #         'P/B Ratio': pb_ratio
    #     }, index=[0])
    #     metrics_df = pd.concat([metrics_df, stock_df], ignore_index=True)


