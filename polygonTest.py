# This is a test file to practice polygon.io REST API

from polygon import RESTClient
from get_all_tickers import get_tickers as gt
import os
import pandas as pd
import datetime
from datetime import date,timedelta
import numpy as np
import time

#Initializes the root db with columns of ticker int ids, ticker names, and last updated time
def init_root_db(tickerList):
    idList = []
    dateList = []
    print('='*50)
    print("Root db ids being created...")
    for i in range(len(tickerList)):
        idList.append(i)
    print("Root db ids have been successfully created.")
    print("Root db dates being created...")
    for i in range(len(tickerList)):
        dateList.append(datetime.date.today())
    print("Root db dates have been successfully created.")
    print('='*50)
    data = list(zip(idList,tickerList,dateList))
    df = pd.DataFrame(data,columns=['id','ticker','lastUpdated'])
    df.to_csv(path_or_buf="Root_Database.csv")
    return 1

def init_info_db(key,tickerList):
    idList = []
    epsList = []
    lastPriceList = []
    yearLowList=[]
    rootData = pd.read_csv(filepath_or_buffer="Root_Database.csv")
    print('='*50)
    print("Info db ids being matched...")
    for index in rootData.index:
        idList.append(rootData.loc[index,'id'])
    print("Info db ids have been successfully matched.")
    print("Info db eps being created...")
    #5 API calls per min
    i = 0
    for ticker in rootData.ticker:
        if i == 4:
            break
        if ticker in tickerList:
            epsList.append(getFinancial(key,ticker,'earningsPerDilutedShare'))
        i+=1
    print("Info db eps have been successfully created.")
    print("Info db previous day close being created...")
    #Additional 5 api calls per min
    i = 0
    time.sleep(50)
    for ticker in rootData.ticker:
        if i == 4:
            break
        if ticker in tickerList:
            resultList = getDailyOpenClose(key,ticker,1)
            lastPriceList.append(resultList[0])
            yearLowList.append(resultList[1])
        i+=1
    print("Info db previous day close have been successfully created.")
    print("Info db 52w low being created...")
    print("Info db 52w low have been successfully created.")
    print('='*50)
    data = list(zip(idList,epsList,lastPriceList,yearLowList))
    df = pd.DataFrame(data,columns=['id','eps','prevClose','yearLow'])
    df.to_csv(path_or_buf="Info_Database.csv")
    print(data)
    return 1

#Takes a ticker name string and the financial spec string {eps,prev day close, 52w low, etc.} and returns the data point
def getFinancial(key,ticker,infoSpec):
    #API CALL
    with RESTClient(key) as client:
        resp = client.reference_stock_financials(ticker,limit=1,type='Q')
        try:
            print(f"{ticker} {infoSpec} is {resp.results[0].get(infoSpec)} as reported on {resp.results[0].get('reportPeriod')}.")
            return resp.results[0].get(infoSpec)
        except:
            print(f"No {infoSpec}.")
            return "DNE"
    return 0

#Takes a ticker name string and status int {0=open,1=close,2=52wlow} and returns the open/close price
def getDailyOpenClose(key,ticker,status):
    #Note that there is a delay between recordings of daily close, ie. find close from previous day not day of
    #API CALL
    with RESTClient(key) as client:
        if status == 0:
            resp = client.stocks_equities_daily_open_close(ticker,convertDateTimeToString(datetime.date.today() - timedelta(days=1)))
            try:
                print(f"{ticker} {status} on: {resp.from_} opened at {resp.open}.")
                return resp.close
            except:
                print(f"No {status} for {ticker}")
                return "DNE"
        elif status == 1:
            refLow = []
            resultList = []
            from_ = convertDateTimeToString(datetime.date.today() - timedelta(days=365))
            to = convertDateTimeToString(datetime.date.today() - timedelta(days=1))
            resp = client.stocks_equities_aggregates(ticker,1,"day",from_,to)
            try:
                for info in resp.results:
                    refLow.append(info.get("l"))
                #resultList{0=prev day close, 1=52wlow}
                prevClose = resp.results[len(resp.results)-1].get("c")
                yearLow = min(refLow)
                resultList.append(prevClose)
                resultList.append(yearLow)
                print(f"{ticker} status: {status}| on: {to}  closed at {str(prevClose)}.")
                print(f"{ticker} status: {status}| 52 week low is {str(yearLow)}.")
                return resultList
            except:
                print(f"No {status} for {ticker}")
                return "DNE"

    return 0

def convertDateTimeToString(inDate):
    if inDate.month < 10:
        month = '0{0}'.format(inDate.month)
    else:
        month = inDate.month
    if inDate.day < 10:
        day = '0{0}'.format(inDate.day)
    else:
        day = inDate.day
    dateString = '{0}-{1}-{2}'.format(inDate.year,month,day)
    return dateString

def main():
    key = 'PjeqU9zauMH9o49WYWurfZslqfY8HpF7'
    #API CALL
    with RESTClient(key) as client:
        
        ''' This block is for reference purposes only
        # Note that Q results are off by 1 fiscal year, bug currently being worked on
        resp = client.stocks_equities_daily_open_close("AAPL","2018-03-02")
        print(f"on: {resp.from_} Apple opened at {resp.open} and closed at {resp.close}")
        resp = client.reference_stock_financials("MSFT",limit=1,type='Q')
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
        '''

        #Get a list of all tickers
        list_of_all_tickers = gt.get_tickers(NYSE=True,NASDAQ=True,AMEX=False)
        
        #Set flags to keep track of db initializations
        DB_EXISTENCE_FLAGS = [False,False,False]

        #Initialize the root db
        if os.path.isfile("Root_Database.csv"):
            print("Root DB found, aborting init operation.")
        else:
            if(init_root_db(list_of_all_tickers)):
                DB_EXISTENCE_FLAGS[0] = True
                print("Root DB has been successfully initialized.")
            else:
                print("Root DB initialization has failed.")
        
        #Initialize the info db
        if os.path.isfile("Info_Database1.csv"):
            print("Info DB found, aborting init operation.")
        else:
            if(init_info_db(key,list_of_all_tickers)):
                DB_EXISTENCE_FLAGS[1] =True
                print("Info DB has been successfully initialied.")
            else:
                print("Info DB initialization has failed.")

        
        #Initialize the ratios db



if __name__ == '--main__':
    main()
