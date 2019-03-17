#Stock data first pass
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader as web
import numpy as np
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

