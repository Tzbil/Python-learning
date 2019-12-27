 
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 22:34:45 2019

@author: Tian Zhang
"""
#aapl.index.get_loc('2018-10-01')

def main():
    import pandas as pd
    aapl = pd.read_csv("AAPL.csv").set_index('Date')
    amzn = pd.read_csv("AMZN.csv").set_index('Date')
    ibm = pd.read_csv("IBM.csv").set_index('Date')

    ## Specify Date Range
    import datetime
    date_range = pd.date_range(start = aapl.index[0], end = aapl.index[-1])
    beg = input("Enter the beginning date between " + aapl.index[0]  + " and " + aapl.index[-1]+": ")

    ### If beg is out of range, prompt user to enter another one
    while beg not in date_range:
        print("Start date is out of the date range")
        beg = input("Enter the beginning date between " + aapl.index[0]  + " and " + aapl.index[-1]+": ")

    ### if there no beg in dataframe, beg =  beg + 1 (date)
    no_such_date = True
    while no_such_date:
        try:
            aapl.loc[beg]
            no_such_date = False
        except:
            beg = str(pd.to_datetime(beg) + datetime.timedelta(days = 1)).split()[0]

    end = input("Enter the beginning date between " + aapl.index[0]  + " and " + aapl.index[-1]+": ")
    ### If end is out of range, prompt user to enter another one
    while pd.to_datetime(end) < pd.to_datetime(beg):
        print("End date cannot be before start date")
        end = input("Enter the ending date after "+beg+": ")

    while end not in date_range:
        print("End date is out of date range")
        end = input("Enter the beginning date between " + aapl.index[0]  + " and " + aapl.index[-1]+": ")

    ### if there no beg in dataframe, end =  end - 1 (date)
    no_such_date = True
    while no_such_date:
        try:
            aapl.loc[end]
            no_such_date = False
        except:
            end = str(pd.to_datetime(end) - datetime.timedelta(days = 1)).split()[0]

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
