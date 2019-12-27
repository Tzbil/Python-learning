#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 21:56:30 2019

@author: Tian Zhang
"""

def main():
    import pandas as pd
    import quandl
    quandl.ApiConfig.api_key = '' # get your free quandl api key on quandl.com
    
    beg = str(pd.to_datetime(input("Enter the begaining date in format yyyy-mm-dd: "))).split()[0]
    end = str(pd.to_datetime(input("Enter the ending date in format yyyy-mm-dd: "))).split()[0]
    
    while pd.to_datetime(end) < pd.to_datetime(beg):
        print("End date cannot be before start date")
        end = input("Enter the ending date after "+beg+": ")
        
    find_next = "y"
    sel = pd.DataFrame()
    symbol = []
    while find_next.lower() == "y":
        ticker = input("Enter the ticker of the stock: ")
        stock = quandl.get((["WIKI/"+ticker+".4"]),start_date= beg, end_date= end,)
        while stock.empty == True:
            print("Stock not found. Please enter another one:")
            ticker = input()
            stock = quandl.get((["WIKI/"+ticker+".4"]),start_date= beg, end_date= end,)
        
        stock = stock.rename(columns = {"WIKI/"+ticker+" - Close":"Close"})
        stock['Symbol'] = ticker
        sel = pd.concat([sel, stock])
        symbol.append(ticker)
        find_next = input("Do you want to find another stock? y for yes ")
    
    pd.options.display.float_format = '{:,.2f}'.format
    

    summary = pd.DataFrame()
    
    summary["Symbol"] = symbol
    summary = summary.set_index("Symbol")
    
    import datetime
    beg_price = []
    end_price = []
    for i in range(len(symbol)):
        no_such_date = True
        while no_such_date:
            try:
                beg_price.append(sel[sel['Symbol'] == symbol[i]].loc[beg]['Close'])
                no_such_date = False
            except:
                beg = str(pd.to_datetime(beg) + datetime.timedelta(days = 1)).split()[0]
                
        no_such_date = True
        while no_such_date:
            try:
                end_price.append(sel[sel['Symbol'] == symbol[i]].loc[end]['Close'])
                no_such_date = False
            except:
                end = str(pd.to_datetime(end) - datetime.timedelta(days = 1)).split()[0]
    
    print("\n\n\n\n\nSummary of stock prices from "+beg+ " to "+end+"\n")

    summary['Begaining Price'] = beg_price
    summary['Ending Price'] = end_price
    
    summary['Minimum'] = sel.groupby("Symbol")["Close"].min()
    summary['Maximum'] = sel.groupby("Symbol")["Close"].max()
    summary['Average'] = sel.groupby("Symbol")["Close"].mean()
    
    print(summary)
    
    import matplotlib.pyplot as plt
    sel.pivot(columns='Symbol',values='Close').plot()
    
    plt.xlabel("Date")
    plt.ylabel("Price($)")
    plt.title("Stock Prices")
    plt.grid(True)
    plt.xticks(rotation = 45)
    

main()
    
    
