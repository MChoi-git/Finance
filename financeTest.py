import yfinance as yf
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="darkgrid")

# Notes:
#   See https://github.com/ranaroussi/yfinance
#   See https://aroussi.com/post/python-yahoo-finance
#   KO,^DJI,^IXIC,AAPL,AMZN,PEP,JNJ,BP,MSFT,XOM

# Export to CSV helper function
def CSV_maker(filename, data):
    with open(filename, 'w') as f:
        for key in data.keys():
            # This breaks any text entry with commas in it
            f.write("%s,%s\n"%(key, data[key]))
    return True

# Creation of ticker to play with
msft = yf.Ticker("MSFT")

# Definition of ticker data we want to look at 
#   -Ticker contains A LOT of garbage vars we don't want
IMPORTANT_TICKER_TYPES = [
        'info',
        'history', # [period,interval,start,end,prepost,auto_adjust,actions]
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
for ele in IMPORTANT_TICKER_TYPES:
    exec("print(type(msft.%s))" % (ele))

graph = sns.relplot(x = 'Date', y='Open',kind='line',data=msft.history(period='max'))
graph.fig.autofmt_xdate()
plt.show()

print(msft.history(period='max'))
# Send to CSV
CSV_maker(".csv", msft.info)
