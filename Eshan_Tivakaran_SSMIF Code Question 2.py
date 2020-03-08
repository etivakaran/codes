#!/usr/bin/env python
# coding: utf-8

# # Question 2

# In[42]:


import sqlite3
import pandas as pd
import pandas_datareader as web
import datetime as dt
import math as m
start = dt.date(2019, 1,1)
end = dt.date(2019,12,31)
#Important Modules to import.
#It is good to have the start and end date labeled as variables.


# In[40]:


#This function Creates the SQLite table.
#Note that if the table is already made, the try-except statement will catch it and
#print that the table was already made.
#This code was directly taken from the SSMIF Coding Assignment Prompt
def Create_Table():
    try:
        conn = sqlite3.connect('SSMIF.db')
        c = conn.cursor()

        c.execute("""CREATE TABLE "Stock_Data" (
                 "Timestamp" INTEGER NOT NULL,
                 "Open" DECIMAL(10, 2),
                 "High" DECIMAL(10, 2),
                 "Low" DECIMAL(10, 2),
                 "Close" DECIMAL(10, 2),
                 "Adj_Close" DECIMAL(10, 2) );""")
        conn.commit()
        conn.close()
    except:
        print("The database is already made.")


# In[43]:


#First I used pandas_datareader to gather all of the prices.
#For this to actually fill the SQLite table, the columns of the dataframe
#must match with the columns of table.  Therefore I renamed and removed some of the
#unimportant columns.  (I could have also gone the traditional route of
#iterating through the dataframe and using the "INSERT INTO" SQLite command.)
#Then I connected to the database and filled it.  I made sure
#to close the database when finished.
def Fill_Table(ticker):
    df = web.DataReader(ticker, "yahoo", start, end)
    df.reset_index(inplace = True, drop = False)
    df = df.rename(columns = {"Date": "Timestamp", "Adj Close": "Adj_Close"})
    df = df.set_index("Timestamp")
    df = df.drop(columns = ["Volume"])

    conn = sqlite3.connect('SSMIF.db')
    c = conn.cursor()

    df.to_sql('Stock_Data', conn, if_exists = 'replace')
    c.execute("SELECT * FROM Stock_Data").fetchall()

    conn.commit()
    conn.close()


# In[37]:


#This is similiar to the version in question #1, except instead of
#reading it from a dataframe, it reads it from a list.
#The algorithm is the same.
def Daily_Returns(close_price):
    daily_returns = []
    for i in range(len(close_price)):
        if i == 0:
            continue
        else:
            daily_returns.append(100 * (close_price[i]/close_price[i - 1] - 1))
    return daily_returns


# In[38]:


#First I connected to the SQLite table
#Then I read all of the Adjusted Close prices in the table.
#When reading it,the values are recorded as tuples-1 in a list.
#I then converted those tuples into floats so they can work with the
#Daily_Returns function built earlier.  After, I got the daily returns, I sorted
#them and found the VaR like I did in the last question.
def Monthly_VaR(conf = .05):
    conn = sqlite3.connect('SSMIF.db')
    c = conn.cursor()

    c.execute("SELECT Adj_Close FROM Stock_Data;")
    results = c.fetchall()

    results = [float(x[0]) for x in results]
    daily_returns = Daily_Returns(results)
    daily_returns = sorted(daily_returns)

    threshold = int(len(daily_returns) * conf)
    daily_VaR = daily_returns[threshold]
    time_factor = 20
    
    return m.sqrt(time_factor) * daily_VaR

