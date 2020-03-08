#!/usr/bin/env python
# coding: utf-8

# # Question 1

# In[4]:


import pandas as pd
import pandas_datareader as web
import datetime as dt
import statistics as s
import math as m
start = dt.date(2019, 1,1)
end = dt.date(2019,12,31)
#Important Modules to import.
#It is good to have the start and end date labeled as variables.


# In[10]:


#The prompt didn't gurantee that the Series "Open" would be available,
#therefore I only used the "Adj Close" Series in the dataframe.
#Otherwise, the formula I would have used to calculate the daily return would be:
#100 * (("Adj Close" / "Open") - 1)
#In this case, I just used the fact that "Adj Close" was available.
#Here I created a list that has all of the daily returns using the formula:
#100 * ((closing price of today / closing price of yesterday) - 1)
#Using a for-loop, I did this for everyday and returned the list.
def Daily_Returns(df):
    daily_returns = []
    for i in range(len(df["Adj Close"])):
        if i == 0:
            continue
        else:
            daily_returns.append(100 * (df["Adj Close"][i]/df["Adj Close"][i - 1] - 1))
    return daily_returns


# In[97]:


#First I used pandas_datareader to gather all of the prices.
#Then I used the prior function to get a list with all of the daily returns.
#The VaR could be understood as the lower bound of a confidence interval,
#so now I just need to find that lower bound given my confidence level (which is an optional parameter).
#By sorting all of the daily returns, I can find the lower bound by multiplying the 
#number of trading days by the confidence level and then rounding down that answer, the threshold value.
#This gives me the number of the worst days, so the VaR would be "the best" of those
#"worst days".  To find the actual VaR, because the list is sorted, the VaR would be the 
#the daily return with the threshold number as its index.
#Finally, to get the monthly VaR, I would need to multiply it by the square root of the number of days,
#which in this case is 20 (because there are typically 20 trading days in a month).
def Monthly_VaR(ticker, conf = .05):
    df = web.DataReader(ticker, 'yahoo', start, end)
    daily_returns = Daily_Returns(df)
    daily_returns = sorted(daily_returns)
    threshold = int(len(daily_returns) * conf)
    daily_VaR = daily_returns[threshold]
    time_factor = 20
    return m.sqrt(time_factor) * daily_VaR


# In[114]:


#First I used pandas_datareader to gather all of the prices.
#Then I used the Daily_Returns function to get a list with all of the daily returns.
#The CVaR could be understood as the weighted average of the tail.
#The tail is the region of returns that are worse than the VaR return
#It could also be understood as the returns that are lower than the lower bound of the
#confidence interval.  Because these are all independent events with equal probabilities,
#the CVaR is a regular average, not a weighted average.
#Therefore, we can just take the mean of all of the returns less than (and not equal to)
#the VaR return.
#Because this answer is a daily CVaR, we must convert it into a monthly CVaR.
#This will be done by multiplying the daily CVaR by the square root of 20,
#the number of trading days in a month.
def Monthly_CVaR(ticker, conf = .05):
    df = web.DataReader(ticker, 'yahoo', start, end)
    daily_returns = Daily_Returns(df)
    daily_returns = sorted(daily_returns)
    threshold = int(len(daily_returns) * conf)
    daily_CVaR = s.mean(daily_returns[:threshold])
    return m.sqrt(20) * daily_CVaR


# In[103]:


#First I used pandas_datareader to gather all of the prices.
#Then I used the Daily_Returns function to get a list with all of the daily returns.
#According to the provided link, the volitility is just the population standard deviation
#of the set of returns, which Python can do easily with a simple function.
#To calculate the monthly volitility, we must multiply the daily volitility by
#the square root of 20, the number of trading days in a month.
def Monthly_Volitility(ticker):
    df = web.DataReader(ticker, 'yahoo', start, end)
    daily_returns = Daily_Returns(df)
    return s.pstdev(daily_returns) * m.sqrt(20)

