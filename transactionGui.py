from tkinter import *
from tkinter import ttk
import time
import datetime
import sessionExecutor

#This file is big and chunky, refactor to use enum+loops you fucking monkey

def transactionWindow():
    #Event handlers
    def closeClicked():
        #Close the program
        root.destroy()
    def helpClicked(obj):
        #Print help information
        print("help")
    def addClicked(argsraw):
        #Add an entry
        args = ['add'] + argsraw
        sessionExecutor.transactionExec(args)
    def removeClicked(argsraw):
        #Remove an entry
        args = ['remove'] + argsraw
        sessionExecutor.transactionExec(args)
    def populateClicked(argsraw):
        #Populate db from csv
        args = ['populate'] + argsraw
        sessionExecutor.transactionExec(args)
    def updateClicked(argsraw):
        #Add entries to db
        args = ['update'] + argsraw
        sessionExecutor.transactionExec(args)
    class TransactionWindow:
        def __init__(self,master):
            #Initialize tkinter
            self.master = master
            master.title("Transaction Window")
            
            #Initialize window variables
            #add func
            self.ticker = StringVar(master, 'ticker')
            self.company_name = StringVar(master, 'company name')
            self.date = StringVar(master, datetime.date.today())
            self.open = IntVar(master, value=0)
            self.high = IntVar(master, value=0)
            self.low = IntVar(master, value=0)
            self.close = IntVar(master, value=0)
            self.volume = IntVar(master, value=0)
            self.debt_to_equity_ratio = DoubleVar(master, value=0)
            self.dividend_yield = DoubleVar(master, value=0)
            self.earnings_per_diluted_share = DoubleVar(master, value=0)
            self.gross_profit = IntVar(master, value=0)
            self.net_income = IntVar(master, value=0)
            self.price_to_earnings_ratio = DoubleVar(master, value=0)
            self.revenues_usd = IntVar(master, value=0)

            #remove func
            self.id = IntVar(master, value=0)

            #populate func
            self.filename = StringVar(master, '')

            #update func
            self.args = [
                    self.ticker,
                    self.company_name,
                    self.date,
                    self.open,
                    self.high,
                    self.low,
                    self.close,
                    self.volume,
                    self.debt_to_equity_ratio,
                    self.dividend_yield,
                    self.earnings_per_diluted_share,
                    self.gross_profit,
                    self.net_income,
                    self.price_to_earnings_ratio,
                    self.revenues_usd,
                    self.id,
                    self.filename
                    ]
            #Setup UI widgets
            #Labels
            self.idLabel = Label(master, text="ID")
            self.idLabel.place(x=10,y=10)
            self.tickerLabel = Label(master, text="Ticker")
            self.tickerLabel.place(x=10,y=50)
            self.company_nameLabel = Label(master, text="Company Name")
            self.company_nameLabel.place(x=10,y=90)
            self.dateLabel = Label(master, text="Date")
            self.dateLabel.place(x=10,y=130)
            self.openLabel = Label(master, text="Open")
            self.openLabel.place(x=10,y=170)
            self.highLabel = Label(master, text="High")
            self.highLabel.place(x=10,y=210)
            self.lowLabel = Label(master, text="Low")
            self.lowLabel.place(x=10,y=250)
            self.closeLabel = Label(master, text="Close")
            self.closeLabel.place(x=10,y=290)
            self.volumeLabel = Label(master, text="Volume")
            self.volumeLabel.place(x=10,y=330)
            self.debt_to_equity_ratioLabel = Label(master, text="Debt to Equity Ratio")
            self.debt_to_equity_ratioLabel.place(x=10,y=370)
            self.dividend_yieldLabel = Label(master, text="Divident Yield")
            self.dividend_yieldLabel.place(x=10,y=410)
            self.earnings_per_diluted_shareLabel = Label(master, text="Earnings per Diluted Share")
            self.earnings_per_diluted_shareLabel.place(x=10,y=450)
            self.gross_profitLabel = Label(master, text="Gross Profit")
            self.gross_profitLabel.place(x=10,y=490)
            self.net_incomeLabel = Label(master, text="Net Income")
            self.net_incomeLabel.place(x=10,y=530)
            self.price_to_earnings_ratioLabel = Label(master, text="PE Ratio")
            self.price_to_earnings_ratioLabel.place(x=10,y=570)
            self.revenues_usdLabel = Label(master, text="Revenues in USD")
            self.revenues_usdLabel.place(x=10,y=610)
            #Buttons
            self.helpButton = Button(master, text="Help", command=helpClicked(self))
            self.helpButton.place(x=700,y=10)
            self.addButton = Button(master, text="Add", command=lambda args = self.args: addClicked(args))
            self.addButton.place(x=700,y=50)
            self.removeButton = Button(master, text="Remove",command=lambda args = self.args: removeClicked(args))
            self.removeButton.place(x=700,y=90)
            self.populateButton = Button(master, text="Populate", command=lambda args = self.args: populateClicked(args))
            self.populateButton.place(x=700,y=130)
            self.updateButton = Button(master, text="Update", command=lambda args = self.args: updateClicked(args))
            self.updateButton.place(x=700,y=170)
            #Text boxes
            self.idEntry = Entry(master, width=50,textvariable=self.id)
            self.idEntry.place(x=190,y=10)
            self.tickerEntry = Entry(master, width=50,textvariable=self.ticker)
            self.tickerEntry.place(x=190,y=50)
            self.company_nameEntry = Entry(master, width=50,textvariable=self.company_name)
            self.company_nameEntry.place(x=190,y=90)
            self.dateEntry = Entry(master, width=50,textvariable=self.date)
            self.dateEntry.place(x=190,y=130)
            self.openEntry = Entry(master, width=50,textvariable=self.open)
            self.openEntry.place(x=190,y=170)
            self.highEntry = Entry(master, width=50,textvariable=self.high)
            self.highEntry.place(x=190,y=210)
            self.lowEntry = Entry(master, width=50,textvariable=self.low)
            self.lowEntry.place(x=190,y=250)
            self.closeEntry = Entry(master, width=50,textvariable=self.close)
            self.closeEntry.place(x=190,y=290)
            self.volumeEntry = Entry(master, width=50,textvariable=self.volume)
            self.volumeEntry.place(x=190,y=330)
            self.debt_to_equity_ratioEntry = Entry(master, width=50,textvariable=self.debt_to_equity_ratio)
            self.debt_to_equity_ratioEntry.place(x=190,y=370)
            self.dividend_yieldEntry = Entry(master, width=50,textvariable=self.dividend_yield)
            self.dividend_yieldEntry.place(x=190,y=410)
            self.earnings_per_diluted_shareEntry = Entry(master, width=50,textvariable=self.earnings_per_diluted_share)
            self.earnings_per_diluted_shareEntry.place(x=190,y=450)
            self.gross_profitEntry = Entry(master, width=50,textvariable=self.gross_profit)
            self.gross_profitEntry.place(x=190,y=490)
            self.net_incomeEntry = Entry(master, width=50,textvariable=self.net_income)
            self.net_incomeEntry.place(x=190,y=530)
            self.price_to_earnings_ratioEntry = Entry(master, width=50,textvariable=self.price_to_earnings_ratio)
            self.price_to_earnings_ratioEntry.place(x=190,y=570)
            self.revenues_usdEntry = Entry(master, width=50,textvariable=self.revenues_usd)
            self.revenues_usdEntry.place(x=190,y=610)


    #Start window loop
    root = Tk()
    root.geometry('800x700')
    transactionWindowObj = TransactionWindow(root)
    root.mainloop()


