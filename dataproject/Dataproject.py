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
import pickle
import numpy as np
from scipy.stats import norm # normal distribution
import matplotlib.pyplot as plt
import ipywidgets as widgets
style.use("ggplot")



#Automating S&P500 - From Yahoo Finance - Close price adjusted for splits, and Adj. Close price is adjusted for both dividends and splits.
def save_sp500_tickers():
    resp = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    soup = bs.BeautifulSoup(resp.text, "lxml")
    table = soup.find("table", {"class": "wikitable sortable"})
    tickers = []
    for row in table.findAll("tr")[1:]:
        ticker = row.findAll("td")[0].text.replace(".","-")
        ticker = ticker[:-1]
        tickers.append(ticker)

    df_tickers = pd.DataFrame(tickers)
    df_tickers.to_csv("tickers.csv")

    with open("sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)
    
        print(tickers)

        return(tickers)
    
save_sp500_tickers()

df_tickers = pd.read_csv("tickers.csv", index_col= 0)
df_tickers.columns = ["Ticker"]
df_tickers.head()


def get_names():
    resp = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    soup = bs.BeautifulSoup(resp.text, "lxml")
    table = soup.find("table", {"class": "wikitable sortable"})
    names = []
    for row in table.findAll("tr")[1:]:
        name = row.findAll("td")[1].text.replace(".","-")
        names.append(name)

    df_names = pd.DataFrame(names)
    df_names.to_csv("names.csv")

    print(names)

get_names()

df_names = pd.read_csv("names.csv", index_col= 0)
df_names.columns = ["Name"]
df_names.head()


def get_sectors():
    resp = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    soup = bs.BeautifulSoup(resp.text, "lxml")
    table = soup.find("table", {"class": "wikitable sortable"})
    sectors = []
    for row in table.findAll("tr")[1:]:
        sector = row.findAll("td")[3].text.replace(".","-")
        sectors.append(sector)

    df_sectors = pd.DataFrame(sectors)
    df_sectors.to_csv("sectors.csv")

    print(sectors)

get_sectors()

df_sectors = pd.read_csv("sectors.csv", index_col= 0)
df_sectors.columns = ["Sector"]
df_sectors.head()

df_names_and_sector = df_names.join(df_sectors, how = "right")
df_names_and_sector.head()

df_tickers_names_sectors = df_tickers.join(df_names_and_sector, how = "right")
df_tickers_names_sectors.head()
#df_tickers_names_sectors.set_index("Ticker", inplace=True)
#df_tickers_names_sectors.head()
df_tickers_names_sectors.values.tolist

with open ("tickers_names_sectors.pickle", "wb") as f:
    pickle.dump(df_tickers_names_sectors, f)



def get_data_from_yahoo(reload_sp500=False):
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')

    start = dt.datetime(2010, 1, 1)
    end = dt.datetime.now()
    for ticker in tickers:
        # just in case your connection breaks, we'd like to save our progress!
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            df = web.DataReader(ticker, "yahoo", start, end) 
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))

get_data_from_yahoo()

def compile_data():
    with open("sp500tickers.pickle", "rb") as f:
        tickers = pickle.load(f)

    main_df = pd.DataFrame()

    #Iterating though all DFs

    for count, ticker in enumerate(tickers):
        df = pd.read_csv("stock_dfs/{}.csv".format(ticker))
        df.set_index("Date", inplace=True)
        df.rename(columns = {"Adj Close": ticker}, inplace=True) #Adj Close takes the categories place in the column - Simple rename
        df.drop(["Open","High","Low","Close","Volume"],1, inplace=True)
    
        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how="outer")
        
        if count % 100 == 0: #Only print #10, #20, #30, etc.
            print(count)
    print(main_df.head())
    main_df.to_csv("sp500_joined_adj_closes.csv")

compile_data()

data_df = pd.read_csv("sp500_joined_adj_closes.csv")
df_stocks.set_index("Date", inplace=True)

print(df_stocks)

#Get sp500 index data

Index_data = web.DataReader("^GSPC", data_source="yahoo", start="1,1,2000")
Index_data.to_csv("IndexData.csv")

df_index_data = pd.read_csv("IndexData.csv", index_col = "Date", parse_dates=True)
df_index_data.rename(columns = {"Adj Close": "S&P500"}, inplace=True)

df_index_data_new = df_index_data["S&P500"]
print(df_index_data_new)

df_index_data_new = df_index_data_new/df_index_data_new[0]*100
print(df_index_data_new)
df_index_data_new.plot()

df_final = df_stocks.join(df_index_data_new, how="left")
print(df_final)

#Widget/plot


ydata = df_final[["ATVI", "S&P500"]].copy()

plt.plot(ydata)

def plot():

    df = df_final
    
    plt.plot(df["ATVI"], label = "Activision Blizzard")
    plt.plot(df["S&P500"], label = "S&P500 Index")

    plt.legend(loc = "upper center", shadow = True, fontsize = "small", facecolor = "black")

    plt.show()


plot()








