import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
plt.style.use('seaborn')

import yfinance as yf
# Alpha vantage code PMC13EMV4SJG0S3D

#Get all the stocks in variables
evgrf= yf.Ticker('evgrf')
aapl = yf.Ticker('aapl')
msft = yf.Ticker('msft')
nttyy = yf.Ticker('nttyy')
goog = yf.Ticker('goog')

#Store all stocks into an array
stocks = [evgrf, aapl, msft, nttyy, goog]

#Print out the data of each to test
# for stock in stocks:
#     print(stock.info)

# pe_ratio, pb_ratio
for stock in stocks:
    stock_symbol = stock.ticker

    #Price / Earnings Ratio
    pe_ratio = stock.info.get('trailingPE', 'N/A')
    print(f"{stock_symbol}: P/E ratio - {pe_ratio}")

    # Price / Book ratio, 0.95-1.1 is normal, 0.5 and below is considered very good
    pb_ratio = stock.info.get('priceToBook', 'N/A')
    print(f"{stock_symbol}: P/B ratio - {pb_ratio}")

    # Debt-To-Equity ratio
    # total_debt = stock.info.get('totalDebt')
    # total_equity = stock.info.get('totalStockholderEquity')
    # debt_to_equity_ratio = 'N/A'
    # if total_debt and total_equity:
    #     debt_to_equity_ratio = total_debt / total_equity
    # print(f"{stock_symbol}: Debt-To-Equity ratio - {debt_to_equity_ratio}")
    
    # Free cash flow

    #
print("hello")



