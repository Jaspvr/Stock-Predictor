import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
# plt.style.use('seaborn')

import yfinance as yf

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/stocks')
def home():

    #ACCESSING INDIVIDUAL STOCKS (Currently this is the top 25 in the S%P 500)
    aapl = yf.Ticker('aapl')
    msft = yf.Ticker('msft')
    amzn = yf.Ticker('amzn')
    nvda = yf.Ticker('nvda')
    tsla = yf.Ticker('tsla')
    googl = yf.Ticker('googl')
    meta = yf.Ticker('meta')
    goog = yf.Ticker('goog')
    # brkb = yf.Ticker('brk-b')
    unh = yf.Ticker('unh')
    jnj = yf.Ticker('jnj')
    jpm = yf.Ticker('jpm')
    xom = yf.Ticker('xom')
    v = yf.Ticker('v')
    lly = yf.Ticker('lly')
    pg = yf.Ticker('pg')
    avgo = yf.Ticker('avgo')
    ma = yf.Ticker('ma')
    hd = yf.Ticker('hd')
    mrk = yf.Ticker('mrk')
    cvx = yf.Ticker('cvx')
    pep = yf.Ticker('pep')
    abbv = yf.Ticker('abbv')
    cost = yf.Ticker('cost')
    ko = yf.Ticker('ko')

    # ACCESSING ALL STOCKS IN S&P
    # sp500_tickers = yf.tickers_sp500()

    # Store all stocks into a dictionary with their symbols as keys
    stocks = {
        'aapl': aapl,
        'msft': msft,
        'amzn': amzn,
        'nvda': nvda,
        'tsla': tsla,
        'googl': googl,
        'meta': meta,
        'goog': goog,
        'brk-b': brkb, 
        'unh': unh,
        'jnj': jnj,
        'jpm': jpm,
        'xom': xom,
        'v': v,
        'lly': lly,
        'pg': pg,
        'avgo': avgo,
        'ma': ma,
        'hd': hd,
        'mrk': mrk,
        'cvx': cvx,
        'pep': pep,
        'abbv': abbv,
        'cost': cost,
        'ko': ko
    }

    # Create an empty dictionary to store the stock data
    # stock_data = {}
    metrics_df = pd.DataFrame(columns=['Ticker', 'P/E Ratio', 'P/B Ratio'])

    # Iterate over each ticker in the S&P 500
    for ticker in stocks:
        # Retrieve the stock data using the ticker symbol
        stock = yf.Ticker(ticker)
        
        # Retrieve the desired metrics
        pe_ratio = stock.info.get('trailingPE', 'N/A')
        pb_ratio = stock.info.get('priceToBook', 'N/A')
        
        # Append the metrics to the DataFrame
        stock_df = pd.DataFrame({
            'Ticker': ticker,
            'P/E Ratio': pe_ratio,
            'P/B Ratio': pb_ratio
        }, index=[0])
        metrics_df = pd.concat([metrics_df, stock_df], ignore_index=True)



    return render_template('index.html', stock_data=metrics_df)

if __name__ == '__main__':
    app.run(debug=True, port = 8000)
