#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 09:22:42 2019

@author: Tian Zhang
"""

def trend(beg,end,symbol):
    '''
    beg & end: string contatn date information. Could be in format '2019-08-19' or 
    '08/19/2019' or '2019/08/19' or '19/08/2019'
    symbol: list concontains stocks' tickers users want to look up
    '''
    import pandas as pd
    import quandl
    quandl.ApiConfig.api_key = '' # get your own free quandl api on quandl.com
    
    beg = str(pd.to_datetime(beg)).split()[0]
    end = str(pd.to_datetime(end)).split()[0]
    
    while pd.to_datetime(end) < pd.to_datetime(beg):
        print("End date cannot be before start date")
        end = input("Enter the ending date after "+beg+": ")
        
    sel = pd.DataFrame()
    for i in range(len(symbol)):
        stock = quandl.get((["WIKI/"+symbol[i]+".4"]),start_date= beg, end_date= end,)
        while stock.empty == True:
            print("Stock not found. Please enter another one:")
            symbol[i] = input()
            stock = quandl.get((["WIKI/"+symbol[i]+".4"]),start_date= beg, end_date= end,)
        
        stock = stock.rename(columns = {"WIKI/"+symbol[i]+" - Close":"Close"})
        stock['Symbol'] = symbol[i]
        sel = pd.concat([sel, stock])
    
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
    
    
    
