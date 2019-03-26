#First pass
"""
write this in the Terminal:
pip install https://github.com/matplotlib/mpl_finance/archive/master.zip

And this:
conda install -c anaconda pandas-datareader

When asked:
The following packages will be SUPERSEDED by a higher-priority channel:

  ca-certificates                                 pkgs/main --> anaconda
  certifi                                         pkgs/main --> anaconda
  openssl                                         pkgs/main --> anaconda
  qt                                              pkgs/main --> anaconda
Proceed ([y]/n)?

Press y
"""
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
import pandas as pd
import pandas_datareader as web
import numpy as np
import bs4 as bs
import pickle
import requests
import os
style.use("ggplot")

#Tesla
start = dt.datetime(2000,1,1)
end = (2016,12,31)

Stock = web.DataReader("TSLA", data_source = "yahoo", start="1/1/2010")
Stock.head(100)

#Tesla.to_excel("TSLA.xls") #Laver en Excel fil
Stock.to_csv("Stock.csv")

#Indlæs en csv fil, og lav datetime index
csv = pd.read_csv("Stock.csv", parse_dates=True, index_col=0)
csv.head(100) #Helt det samme som før, bare en anden metode

csv['Adj Close'].plot()
csv['Open'].plot()

print(csv[["Open", "High"]].head(20))

csv["100ma"] = csv["Adj Close"].rolling(window=100, min_periods=0).mean()    #100 moving average - pris idag, og 99 forrige priser.

csv.head(10)
csv.tail(10)

#Multiple plots

ax1 = plt.subplot2grid((6,1), (0,0), rowspan= 5, colspan=1)  #6 rows, 1 column. Starts at (0,0) and spans over|
ax2 = plt.subplot2grid((6,1), (5,0), rowspan= 5, colspan=1, sharex = ax1)

ax1.plot(csv.index, csv["Adj Close"])
ax1.plot(csv.index, csv["100ma"])
ax2.plot(csv.index, csv["Volume"])

#Resampling data
Stock_ohlc = csv["Adj Close"].resample("10D").ohlc() #Ohlc = Open, high, low, close. 10D = 10 days
Stock_volume = csv["Volume"].resample("10D").sum()

Stock_ohlc.head()

Stock_ohlc.reset_index(inplace=True)

#Convert to mdates and candlestick
Stock_ohlc = csv["Adj Close"].resample("10D").ohlc() #Ohlc = Open, high, low, close. 10D = 10 days
Stock_volume = csv["Volume"].resample("10D").sum()
Stock_ohlc.reset_index(inplace=True)

Stock_ohlc["Date"] = Stock_ohlc["Date"].map(mdates.date2num)

ax1 = plt.subplot2grid((6,1), (0,0), rowspan= 5, colspan=1)  
ax2 = plt.subplot2grid((6,1), (5,0), rowspan= 5, colspan=1, sharex = ax1)
ax1.xaxis_date()

candlestick_ohlc(ax1,Stock_ohlc.values, width=2, colorup="g")
ax2.fill_between(Stock_volume.index.map(mdates.date2num), Stock_volume.values, 0)
plt.show() #Candlestick and volume on the lower graph


#Automating S&P500 - From Yahoo Finance - Close price adjusted for splits, and Adj. Close price is adjusted for both dividends and splits.
def save_sp500_tickers():
    resp = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    soup = bs.BeautifulSoup(resp.text, "lxml")
    table = soup.find("table", {"class": "wikitable sortable"})
    tickers = []
    for row in table.findAll("tr")[1:]:
        ticker = row.findAll("td")[1].text.replace(".","-")
        tickers.append(ticker)

    with open("sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)

        print(tickers)

        return(tickers)

save_sp500_tickers()

def save_sp500_names():
    resp_names = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    soup_names = bs.BeautifulSoup(resp_names.text, "lxml")
    table_names = soup_names.find("table", {"class": "wikitable sortable"})
    names = []
    for row in table_names.findAll('tr')[1:]:
        name = row.findAll('td')[0].text.replace('.','-')
        names.append(name)

    with open("sp500names.pickle", "wb") as n:
        pickle.dump(names, n)

        print(names)

        return(names)

save_sp500_names()

def sp500_GICS_sectors():
    resp_gics = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    soup_gics = bs.BeautifulSoup(resp_gics.text, "lxml")
    table_gics = soup_gics.find("table", {"class": "wikitable sortable"})
    gics_sectors = []
    for row in table_gics.findAll("tr")[1:]:
        gics_sector = row.findAll("td")[3].text.replace(".","-")
        gics_sectors.append(gics_sector)

    with open("sp500GICS.pickle","wb") as g:
        pickle.dump(gics_sectors, g)

        print(gics_sectors)

        return(gics_sectors)

sp500_GICS_sectors()

#Getting data from Yahoo
def data_yahoo(reload_sp500=False):
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)

    if not os.path.exists("stock_dfs"):
        os.makedirs("stock_dfs")

    start = dt.datetime(2000,1,1)
    end = dt.datetime.now()
    for ticker in tickers:
        if not os.path.exists("stock_dfs/{}.csv".format(ticker)):
            df = web.DataReader(ticker, "yahoo", start, end)
            df.to_csv("stock_dfs/{}.csv".format(ticker))
        else:
            print("Already have {}".format(ticker))

data_yahoo()

#Combining all DFs into one single Dataframe

def compile_data():
    with open("sp500tickers.pickle", "rb") as f:
        tickers = pickle.load(f)

    main_df = pd.DataFrame()

    #Iterating though all DFs

    for count, ticker in enumerate(tickers):
        df = pd.read_csv("stock_dfs/{}.csv".format(ticker))
        df.set_index("Date", inplace=True)
        df.rename(columns = {"Adj Close": ticker}, inplace=True) #Adj Close takes the Tickers place in the column - Simple rename
        df.drop(["Open","High","Low","Close","Volume"],1, inplace=True)

        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how="outer")
        
        if count % 10 == 0: #Only print #10, #20, #30, etc.
            print(count)
    print(main_df.head())
    main_df.to_csv("sp500_joined_adj_closes.csv")

compile_data()

#Combining 

#Scale y-axis wrt. Adj. Close prices. 
