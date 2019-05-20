"""
write this in the Terminal:
conda install -c anaconda pandas-datareader

When asked:
The following packages will be SUPERSEDED by a higher-priority channel:

  ca-certificates                                 pkgs/main --> anaconda
  certifi                                         pkgs/main --> anaconda
  openssl                                         pkgs/main --> anaconda
  qt                                              pkgs/main --> anaconda
Proceed ([y]/n)?

Press y

Install dash

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
import dash
import dash_core_components as dcc
import dash_html_components as html
from scipy.stats import norm # normal distribution
import matplotlib.pyplot as plt
import ipywidgets as widgets
style.use("ggplot")

"""The purpose of the code below is to first get the tickers for each of the companites on the S&P500 index list, which we later on will
use to append all the historic data to the appropriate ticker. We use *requests.get* to access the data from Wikipedia, which is the list of tickers, after which we use *BeautifulSoup* to then read the HTML format of the website, and make a table. The *soup.find* command is used to specify where exactly in the HTML the table we want is located. 

We make an empty list, and use a for loop to read all entries in the column of the tickers and append each of these to the list we made (called tickers). 

We save it as a pickle as we want to access this data later on, and fast. We called this *"sp500tickers.pickle"*. """


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

    start = dt.datetime(2016, 1, 1)
    end = dt.datetime.now()
    for ticker in tickers:
        # just in case your connection breaks, we'd like to save our progress!
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            df = web.DataReader(ticker, "yahoo", start, end) 
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))

get_data_from_yahoo()

"""Furthermore, the data from yahoo and the tickers are not very useful by themselves, so obvisouly we want to compile the data in order to get a dataframe with all tickers and their data. We open the pickle file again, and make an empty dataframe.

We can then compile each ticker with their data. We drop all columns that are not *Adj Close*, and rename *Adj Close* to the ticker name since we do not have any other data than for Adjusted Close price. We choose to only include this, since the Adjusted Close price takes into account payment of dividends of companies, eventual stock splits, and Rights offerings.

For easier comparison, we also index the data by dividing the first observation in each column by the rest of the column. 

We then use the empty data frame made before, and join all the data together into a single data frame. 

We also convert the data frame to a csv file for easy access to it. 

finally, we create a data frame from the CSV file just saved, and index the date. We call this new data frame *df_stocks*."""


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
data_df = data_df.drop(["BHGE", "DWDP", "TPR", "ARNC", "ZBH", "OKE", "EVRG", "COST", "EW", "BBT", "JNJ", "VMC", "LIN", "COTY", "DGX", "ZBH", "FTV", "LW"], axis=1)
data_df.set_index("Date", inplace=True)
print(data_df.head())

data_df_indexed = data_df/data_df.iloc[0]*100
print(data_df_indexed)

#First difference of the data
first_difference = data_df_indexed.apply(lambda x: x - x.shift(1))
first_difference = first_difference.fillna(value=0)
first_difference.head() 

#pct. change on the closing prices. 
pct_change = data_df.apply(lambda x: (x - x.shift(1))/x.shift(1)*100)
pct_change = pct_change.fillna(value=0)
pct_change.head() 







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

df_final = data_df.join(df_index_data_new, how="left")
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


#For the exam: Compare sectors as a whole by indexing data for each of the sectors (Index the GIGS) - Make widget where you can pick and choose what to compare.
#Correlation table the stocks (Sectors) 
#Find or make benchmark - beta values and error tracking. 
#


