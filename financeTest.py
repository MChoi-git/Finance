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
#   -CSV maker now throws every pandas dataframe into a file
#   -Minimize polling on yahoo finance
#       -Store and retrieve data mainly from csv (or db)
#           -Create update function in order to update the csv or db
#       -Narrow down specific ticker datatypes that we need instead of trying to handle everything


''' ***DEPRECATED
def CSV_maker(filename, ticker):
    with open(filename, 'w') as f:
    # Go through dataypes in Ticker obj
        for key in ticker.info.keys():
            f.write("%s,%s\n"%(key, ticker.info[key]))
    print("\n")
    return True
'''


# CSV output function
def CSV_maker_df(ticker,ticker_string):
    i = 0
    # Gen expression to filter out garbage attributes
    gen = (attr for attr in dir(ticker) if not callable(getattr(ticker, attr)) and not attr.startswith("__") and not attr.startswith("_") and 
            (isinstance(getattr(ticker,attr),pd.DataFrame) or isinstance(getattr(ticker,attr),dict)))
    for attr in gen:
        if isinstance(getattr(ticker,attr),pd.DataFrame):
            print("%s -> %s put in CSV with extension: %i"%(ticker_string,attr,i))
            # Saving dataframes with non-descript filenames temporarily
            getattr(ticker,attr).to_csv(path_or_buf="%s_%i.csv"%(ticker_string,i))
            i+=1
        if isinstance(getattr(ticker,attr),dict):
            print("%s -> %s put in CSV with extension: %i"%(ticker_string,attr,i))
            with open("%s_%i.csv"%(ticker_string,i),'w') as f:
                for key in getattr(ticker,attr).keys() :
                    f.write("%s,%s\n"%(key,getattr(ticker,attr)[key]))
            i+=1


# Read from CSV
def update_Tickers(ticker_list, filename, time_period):
    df_list = list()
    for ticker in ticker_list:
        data = yf.download(ticker, group_by='Ticker', period=time_period)
        data['ticker'] = ticker
        df_list.append(data)
    df = pd.concat(df_list)
    df.to_csv(filename)
    return df


# Plot specific ticker data 
def plotter(ticker, target_attr):
    # Filter illegal target attributes
    gen = (attr for attr in dir(ticker) if not callable(getattr(ticker, attr)) and not attr.startswith("__") and not attr.startswith("_") and attr 
            == target_attr)
    graph = sns.relplot(x='Date',y='Gross Profit',kin='line',data=getattr(ticker, gen)[6])


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
WATCHED_TICKERS = [
        'MSFT',
        '^DJI',
        '^IXIC',
        'AAPL']
'''       
        'AMZN',
        'PEP',
        'JNJ',
        'BP',
        'XOM',
        'M'
        ]
'''

############################################ Setup ticker lists ########################################
ticker_objects = []
ticker_filenames = []


# Populate Ticker object list
for ticker in WATCHED_TICKERS:
    ticker_objects.append(yf.Ticker(ticker))


# Record .csv output filenames
for ticker in WATCHED_TICKERS:
    ticker_filenames.append("%s.csv" % (ticker))

########################################################################################################    


########################################### Main #######################################################

# Create plots for each Ticker
'''
for ticker in ticker_objects:
    # Create plots and display during runtime
    graph = sns.relplot(x = 'Date', y='Open',kind='line',data=ticker.history(period='max'))
    graph.fig.autofmt_xdate()
    plt.show()
'''

  

msft = yf.Ticker("MSFT")
aapl = yf.Ticker("AAPL")
jnj = yf.Ticker("JNJ")
pep = yf.Ticker("PEP")

print('='*80 + '\nTesting dataframe accessors for Ticker: MSFT \n' + '='*80)
print("\nRow index:")
print(msft.quarterly_financials.index)
print("\nColumn index:")
print(msft.quarterly_financials.columns)
print("\nRetrieving Net Income...")
print("Type of data:")
print(type(msft.quarterly_financials.loc['Net Income']))
print(msft.quarterly_financials.loc['Net Income'])
print(msft.quarterly_financials.loc['Net Income'])
print("\nRetrieving Gross Profit...")
print(msft.quarterly_financials.loc['Gross Profit'])
#print("\nPlotting Net Income and Gross Profit...")
print("\nRetrieving 52 week high...")
print(msft.info.get('regularMarketDayLow'))
print("\nRetrieving P/E ratio...")
print(msft.info.get('trailingPE'))
print("Testing completed.")

print("\nTesting multi-ticker 52w low vs. PE...")
print("\nRetrieving MSFT details...")
print("MSFT 52w low:")
print(msft.info.get('regularMarketDayLow'))
print(msft.info.get('trailingPE'))
print("AAPL 52w low:")
print(aapl.info.get('regularMarketDayLow'))
print(aapl.info.get('trailingPE'))
print("JNJ 52w low:")
print(jnj.info.get('regularMarketDayLow'))
print(jnj.info.get('trailingPE'))
print("PEP 52w low:")
print(pep.info.get('regularMarketDayLow'))
print(pep.info.get('trailingPE'))
print("Testing completed.")


#all_ticker_df = update_Tickers(WATCHED_TICKERS, 'all_watched_ticker_data.csv', 'max')


#graph = sns.relplot(x='Date',y='Gross Profit',kin='line',data=msft.quarterly_financials.loc['Net Income'])
#plotter(msft, 'quarterly_financials')
#plotter(msft, 'quarterly_financials')
#graph.fig.autofmt_xfate()
#plt.show()

# Send pandas dataframe items to .csv
CSV_maker_df(msft,"msft")

'''
# Find important variable types
gen = (attr for attr in dir(msft) if not callable(getattr(msft, attr)) and not attr.startswith("__") and not attr.startswith("_") and isinstance(getattr(msft,attr),pd.DataFrame))
for attr in gen:
    print(getattr(msft,attr))
'''






