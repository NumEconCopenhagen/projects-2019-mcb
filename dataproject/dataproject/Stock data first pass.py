#First pass
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

Tesla = web.DataReader("TSLA", data_source = "yahoo", start="1/1/2010")
Tesla.head(100)

#Tesla.to_excel("TSLA.xls") #Laver en Excel fil
Tesla.to_csv("TSLA.csv")

#Indlæs en csv fil, og lav datetime index
csv = pd.read_csv("TSLA.csv", parse_dates=True, index_col=0)
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
Tesla_ohlc = csv["Adj Close"].resample("10D").ohlc() #Ohlc = Open, high, low, close. 10D = 10 days
Tesla_volume = csv["Volume"].resample("10D").sum()

Tesla_ohlc.head()

Tesla_ohlc.reset_index(inplace=True)

#Convert to mdates and candlestick
Tesla_ohlc = csv["Adj Close"].resample("10D").ohlc() #Ohlc = Open, high, low, close. 10D = 10 days
Tesla_volume = csv["Volume"].resample("10D").sum()
Tesla_ohlc.reset_index(inplace=True)

Tesla_ohlc["Date"] = Tesla_ohlc["Date"].map(mdates.date2num)

ax1 = plt.subplot2grid((6,1), (0,0), rowspan= 5, colspan=1)  
ax2 = plt.subplot2grid((6,1), (5,0), rowspan= 5, colspan=1, sharex = ax1)
ax1.xaxis_date()

candlestick_ohlc(ax1,Tesla_ohlc.values, width=2, colorup="g")
ax2.fill_between(Tesla_volume.index.map(mdates.date2num), Tesla_volume.values, 0)
plt.show() #Candlestick and volume on the lower graph


#Automating S&P500 
def save_sp500_tickers():
    resp = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    soup = bs.BeautifulSoup(resp.text, "lxml")
    table = soup.find("table", {"class": "wikitable sortable"})
    tickers = []
    for row in table.findAll("tr")[1:]:
        ticker = row.findAll("td")[0].text
        tickers.append(ticker)

    with open("sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)

        print(tickers)

        return(tickers)

save_sp500_tickers()

def data_yahoo(reload_sp500=False):
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)

    if not os.path.exists("stock_dfs"):
        os.makedirs("stock_dfs")

start = (2013,1,1)
end = (2018,12,31)

for ticker in tickers:
    if not os.path.exists("stock_dfs/{}.csv".format(ticker)):
        df = web.DataReader(ticker, "yahoo", start)
        df.to_csv("stock_dfs/{}.csv".format(ticker))
    else:
        print("Already have {}".format(ticker))
