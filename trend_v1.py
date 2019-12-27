#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 23:51:57 2019

@author: Tian Zhang
"""
def main():
    import pandas as pd
    aapl = pd.read_csv("AAPL.csv").set_index('Date')
    amzn = pd.read_csv("AMZN.csv").set_index('Date')
    ibm = pd.read_csv("IBM.csv").set_index('Date')

    ## Specify Date Range
    date_range = pd.date_range(start = aapl.index[0], end = aapl.index[-1])
    beg = input("Enter the beginning date between " + aapl.index[0]  + " and " + aapl.index[-1]+": ")

    no_such_date = True
    while no_such_date:
        try:
            aapl.loc[beg]
            no_such_date = False
        except:
            print("No such Date in table! Enter another one:")
            beg = input()

    while beg not in date_range:
        print("Start date is out of the date range")
        beg = input("Enter the beginning date between " + aapl.index[0]  + " and " + aapl.index[-1]+": ")

    end = input("Enter the beginning date between " + aapl.index[0]  + " and " + aapl.index[-1]+": ")

    while pd.to_datetime(end) < pd.to_datetime(beg):
        print("End date cannot be before start date")
        end = input("Enter the ending date after "+beg+": ")

    while end not in date_range:
        print("End date is out of date range")
        end = input("Enter the beginning date between " + aapl.index[0]  + " and " + aapl.index[-1]+": ")

    no_such_date = True
    while no_such_date:
        try:
            aapl.loc[end]
            no_such_date = False
        except:
            print("No such Date in table! Enter another one:")
            end = input()

    aapl['Symbol'] = "AAPL"
    amzn['Symbol'] = "AMZN"
    ibm['Symbol'] = "IBM"

    sel = pd.concat([aapl.loc[beg:end],amzn.loc[beg:end], ibm.loc[beg:end]])
    pd.options.display.float_format = '{:,.2f}'.format

    print("\n\n\n\n\nSummary of stock prices from "+beg+ " to "+end+"\n")
    summary = pd.DataFrame()

    summary["Symbol"] = ['AAPL', 'AMZN', 'IBM']
    summary = summary.set_index("Symbol")

    summary['Begaining Price'] = [aapl.loc[beg]['Adj Close'],
           amzn.loc[beg]['Adj Close'],
           ibm.loc[beg]['Adj Close']]
    summary['Ending Price'] = [aapl.loc[end]['Adj Close'],
           amzn.loc[end]['Adj Close'],
           ibm.loc[end]['Adj Close']]

    summary['Minimum'] = sel.groupby("Symbol")["Adj Close"].min()
    summary['Maximum'] = sel.groupby("Symbol")["Adj Close"].max()
    summary['Average'] = sel.groupby("Symbol")["Adj Close"].mean()


    print(summary)

    import matplotlib.pyplot as plt
    sel.pivot(columns='Symbol',values='Adj Close').plot()

    plt.xlabel("Date")
    plt.ylabel("Price($)")
    plt.title("Stock Prices")
    plt.grid(True)
    plt.xticks(rotation = 45)


main()

### Valid Example
# beg = 2016-10-03
# end = 2018-10-03

### Annoying Example
# beg = 2011-05-28
# beg = 2011-05-29
# beg = 2011-05-30

# end = 2015-01-17
# end = 2015-01-18
# end = 2015-01-19
