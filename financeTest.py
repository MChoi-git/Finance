import yfinance as yf
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="darkgrid")
from collections.abc import Mapping

# Notes:
#   See https://github.com/ranaroussi/yfinance
#   See https://aroussi.com/post/python-yahoo-finance
#   Ticker.info is <dict> where keys are strings but values are mixed
#       -Handle this as a special case

# Export to CSV helper function
#   Received a filename and a Ticker, clears and writes a .csv on every data type listed in IMPORTANT_TICKER_TYPES
#       -Currently only works to send Ticker.info to .csv, add functionality to send all ticker datatypes 
def CSV_maker(filename, ticker):
    with open(filename, 'w') as f:
    # Go through dataypes in Ticker obj
        for key in ticker.info.keys():
            f.write("%s,%s\n"%(key, ticker.info[key]))

    print("\n")
    return True

# Convert dict to pandas dataframe
#   -Probably doesn't work with dicts of mixed value types, idk I'm too tired to experiment rn
def dict_to_df(dict):
    df = pd.DataFrame.from_dict(dict)

# Definition of ticker data we want to look at 
#   -Ticker contains A LOT of garbage vars we don't want
IMPORTANT_TICKER_TYPES = [
        'info',
        'history', # {period,interval,start,end,prepost,auto_adjust,actions}
        'actions',
        'dividends',
        'splits',
        'financials',
        'quarterly_financials',
        'major_holders',
        'institutional_holders',
        'balance_sheet',
        'quarterly_balance_sheet',
        'cashflow',
        'quarterly_cashflow',
        'earnings',
        'quarterly_earnings',
        'sustainability',
        'recommendations',
        'calendar',
        'isin',
        'options',
        'option_chain' # ('yyyy-mm-dd') -> must specify specific expiration
        ]

# Definition of watched tickers
# KO,^DJI,^IXIC,AAPL,AMZN,PEP,JNJ,BP,MSFT,XOM

WATCHED_TICKERS = [
        'MSFT',
        '^DJI',
        '^IXIC',
        'AAPL',
        'AMZN',
        'PEP',
        'JNJ',
        'BP',
        'XOM',
        'M'
        ]

############################################ Main ########################################
ticker_objects = []
ticker_filenames = []

# Populate Ticker object list
for ticker in WATCHED_TICKERS:
    ticker_objects.append(yf.Ticker(ticker))

# Create plots for each Ticker
'''
for ticker in ticker_objects:
    # Create plots and display during runtime
    graph = sns.relplot(x = 'Date', y='Open',kind='line',data=ticker.history(period='max'))
    graph.fig.autofmt_xdate()
    plt.show()
'''

# Record .csv output filenames
for ticker in WATCHED_TICKERS:
    ticker_filenames.append("%s.csv" % (ticker))
print(ticker_filenames)

msft = yf.Ticker("MSFT")
print(msft.info)

# Output each ticker to csv
'''
for filename, ticker in zip(ticker_filenames, ticker_objects):
    if not CSV_maker(filename, ticker):
        print("CSV conversion failed: %s\n"%(filename))
'''

# Find important variable types
for ele in IMPORTANT_TICKER_TYPES:
    exec("print(type(ticker_objects[0].%s))" %(ele))








