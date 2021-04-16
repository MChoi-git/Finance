# This is a test file to practice polygon.io REST API

from polygon import RESTClient
from get_all_tickers import get_tickers as gt
import os
import pandas as pd
import datetime

def init_root_db(tickerList):
    idList = []
    dateList = []
    print("Root db ids being created...")
    for i in range(len(tickerList)):
        idList.append(i)
    print("Root db ids have been successfully created.")
    print("Root db dates being created...")
    for i in range(len(tickerList)):
        dateList.append(datetime.date.today())
    print("Root db dates have been successfully created.")
    data = list(zip(idList,tickerList,dateList))
    df = pd.DataFrame(data,columns=['id','ticker','lastUpdated'])
    df.to_csv(path_or_buf="Root_Database.csv")
    return 1

def main():
    key = 'PjeqU9zauMH9o49WYWurfZslqfY8HpF7'
    with RESTClient(key) as client:
        #resp = client.stocks_equities_daily_open_close("AAPL","2018-03-02")
        #print(f"on: {resp.from_} Apple opened at {resp.open} and closed at {resp.close}")
        resp = client.reference_stock_financials("MSFT",limit=1,type='Q')
        # Note that Q results are off by 1 fiscal year, bug currently being worked on
        print(f"MSFT market cap is {resp.results[0].get('marketCapitalization')} as reported on {resp.results[0].get('reportPeriod')}.")
        custom_limit=100
        resp = client.reference_stock_financials("MSFT",limit=100,type='Q')
        for i in range(custom_limit):
            print('*'*50)
            print(f"MSFT market cap is {resp.results[i].get('marketCapitalization')} as reported on {resp.results[i].get('reportPeriod')}.")
            print(f"MSFT debt to equity ratio is {resp.results[i].get('debtToEquityRatio')} as reported on {resp.results[i].get('reportPeriod')}.")
            print(f"MSFT divident yield is {resp.results[i].get('dividendYield')} as reported on {resp.results[i].get('reportPeriod')}.")
            print(f"MSFT gross profit is {resp.results[i].get('grossProfit')} as reported on {resp.results[i].get('reportPeriod')}.")
            print(f"MSFT net income is {resp.results[i].get('netIncome')} as reported on {resp.results[i].get('reportPeriod')}.")
            print(f"MSFT revenues in USD is {resp.results[i].get('revenuesUSD')} as reported on {resp.results[i].get('reportPeriod')}.")
            print(f"MSFT operating income is {resp.results[i].get('operatingIncome')} as reported on {resp.results[i].get('reportPeriod')}.")
            print('*'*50)

        print("Testing completed for stock financials. Beginning testing for databasing.")
        print("="*50)
        
        # Get a list of all tickers
        list_of_all_tickers = gt.get_tickers(NYSE=True,NASDAQ=True,AMEX=False)
        
        DB_EXISTENCE_FLAGS = [False,False,False]

        if os.path.isfile("Root_Database.csv"):
            print("Root DB found, aborting init operation.")
        else:
            if(init_root_db(list_of_all_tickers)):
                DB_EXISTENCE_FLAGS[0] = True
                print("Root DB has been successfully initialized.")
            else:
                print("Root DB initialization has failed.")

if __name__ == '--main__':
    main()
