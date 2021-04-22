# Database creation script
# Running this script creates the database in CSV format containing the following attributes:
# Root Database
# -ID               int
# -ticker           string
# -lastUpdated      DateTime
# Each ticker will also have additional CSVs created containing the following attributes:
# 1.Info 
#   -ID             int
#  X-info           Dict        <--Keeping up to date is difficult due to size (>2000 tickers)
#   -PE             float
#   -yearLow        float
#   -lastUpdated    DateTime
# 2.Price_History
#   -ID             int
#   -priceHistory   pd.DataFrame
#   -lastUpdated
#
# Current Progress
#   -Root DB successfully created   
#   -Root DB verification and update functions to be implemented later (when its worth the work to do so, root DB is relatively small)
#   -Begin Info DB
#   -Begin Price_History DB
#   -Whole databasing service assumes no ticker is deleted/added for now
#       -Dynamic database editing is too complicated and out of scope for now
# Notes: 
#   -This file is in its final format, no more changes will happen
#   -This will only be used a reference for future projects (probably not, yf sucks)



import pandas as pd
import yfinance as yf
import numpy as np
import csv
import datetime
from get_all_tickers import get_tickers as gat
import os

# Initialize the root database described above, should be run only once
# ID:ticker pair are immutable
# Args: tickerList<List>
# Returns 1 on success, else returns 0
def init_root_database(tickerList):
    # Create a pandas dataframe: columns=[ID,ticker,lastUpdated]
    idList = []
    dateList = []
    print("Root DB ids being created: ")
    for i in range(0,len(tickerList)):
        idList.append(i)
    print("Root DB dates being created: ")
    for i in range(0,len(tickerList)):
        dateList.append(datetime.date.today())
    data = list(zip(idList,tickerList,dateList))
    df =  pd.DataFrame(data,columns=['id','ticker','lastUpdated'])
    df.to_csv(path_or_buf="Root_Database.csv")
    return 1

# Verify that the root database tickers match the list, and that the lastUpdated fields are all current (resolution based on day)
# Args: tickerList<List>
# Returns 1 if current, else returns dict of tickers to be (added=0,deleted=-1,updated=1)
# Finish this shit later, not worth doing right now
def verify_root_databse(currentTickerList): 
    df = pd.read_csv(path_or_buf="Root_Database.csv")
    #for i in range(0, max(len(currentTickerList),len(df.columns))):
    return 1

# Update the root databse 
# Jump to each ticker in changeList and do operation based on opcode
# Args: changeDict<Dict>
# Returns 1 on success, else returns 0
def update_root_database(changeDict):
    return 1

# Initialize the info database described above, should only be run once (update function takes care after)
# Args: tickerList<List>
# Returns 1 on success, else returns 0
def init_info_database(tickerList):
    idList = []
    tickerObjList = []
    PEList = []
    yearLowList = []
    dateList = []
    # Create list of ticker IDs
    print("Ticker ids list being created: ")
    for i in range(0,len(tickerList)):
        idList.append(i)
    print("Ticker ids list has been successfully created.")
    # Create list of ticker objects
    print("Ticker objects being created: ")
    for ticker in tickerList:
        tickerObjList.append(yf.Ticker(ticker))
    print("Ticker objects have been successfully created.")
    # Create list of ticker PE ratios
    print("Listing PE ratios: ")
    for ticker in tickerObjList:
        PEList.append(ticker.info.get('trailingPE'))
        print(ticker.info.get('trailingPE'))
    print("PE list has been successfully created.")
    # Create list of ticker 52 week lows
    print("List of 52w lows being created: ")
    for ticker in tickerObjList:
        yearLowList.append(ticker.info.get('regularMarketDayLow'))
    print("List of 52w lows has been successfully created.")
    # Create last updated column
    for i in range(0,len(tickerList)):
        dateList.append(datetime.date.today())
    data = list(zip(idList,PEList,yearLowList,dateList))
    df = pd.DataFrame(data, columns=['id','pe','52wlow','lastUpdated'])
    df.to_csv(path_or_buf="Info_Database.csv")
    return 1

# Verify that each ticker in the info database is up to date
# Args: None
# Returns 1 on success, else returns 0
# Only checks the lastUpdated field for now
def verify_info_database(currentTickerList):
    return 1

# Update the info database
# Jump to each ticker in changeList and do operation based on opcode
# Args: changeDict<Dict>
# Returns 1 on success, else returns 0
def update_info_database(changeDict):
    return 1



# Main

# Put all tickers in a list
list_of_all_tickers = gat.get_tickers(NYSE=True,NASDAQ=True, AMEX=False)

# Initialize the root DB csv file
# -Once initialized and the csv database is created, 
#       1. init_root_database should never be called again
#       2. The root database should only be read from once created 
#           -Dynamically updating the database is too complicated and outside of scope for now 

DB_EXISTENCE_FLAGS = [False,False,False]

if os.path.isfile("Root_Database.csv"):
    print("Root DB found.")
else:
    if(init_root_database(list_of_all_tickers)):
        DB_EXISTENCE_FLAGS[0] = True
        print("Root DB has been successfully initialized.")
    else:
        print("Root DB initialization has failed.")

if os.path.isfile("Info_Database.csv"):
    print("Info DB found.")
else:
    if(init_info_database(list_of_all_tickers)):
        DB_EXISTENCE_FLAGS[1] = True
        print("Info DB has been successfully initialized.")
    else:
        print("Info DB initialization has failed.")
