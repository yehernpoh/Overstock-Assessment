# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
import pandas as pd
import matplotlib.pyplot as plt


#QUESTION 1
os.chdir("C:\Users\yehernp\OneDrive - Intel Corporation\Desktop")

#getting current dir info
os.getcwd()

#Reading excel sheet
df = pd.read_excel (r'C:\Users\yehernp\OneDrive - Intel Corporation\Desktop\overstock.xlsx')
#Re-indexing and setting Date as the Index
df.set_index('Date', inplace=True)
print (df)

#Displaying top 10 records
df.head(10)


#QUESTION 2
#Creating dataframe that has subset data where channel = unidentified and cutomer_type= existing
unidentified_exist = df[(df.Channel == 'Unidentified') & (df.Customer_Type == 'EXISTING')]

#Visualizing Existing Customers from Unidentified Channel
unidentified_exist.plot(y="Customer_Count")

#Assigning data of different months to separate dataframes. Using index as a filter to segregate data
first_month=unidentified_exist.loc['2017-01'].reset_index()
second_month=unidentified_exist.loc['2017-02'].reset_index()
third_month=unidentified_exist.loc['2017-03'].reset_index()

#Plotting Trend of different Months 
plt.plot(first_month.index, first_month['Customer_Count'], color='blue', linewidth=4,label='first_month')
plt.plot(second_month.index, second_month['Customer_Count'], color='green', linewidth=4,label='second_month')
plt.plot(third_month.index, third_month['Customer_Count'], color='red', linewidth=4,label='third_month')
plt.legend()

#Summing by Marketing_spend
unidentified_exist["Marketing_Spend"].sum(axis=0)

#Averaging by Marketing_spend
unidentified_exist["Marketing_Spend"].mean(axis=0)


#QUESTION 3
#Creating dataframe that has channel= brand
brand = df[(df.Channel == 'Brand')].reset_index()

#Pivoting dataframe to have Customer Type (Existing, New) as the columns
brand_pivot = brand.pivot(index="Date", columns="Customer_Type", values=["Customer_Count"])

#Adding new columns in dataframe that contains Cum of Customer_Count. Filling missing values with zero.
brand_pivot['cum_NEW'] = brand_pivot['Customer_Count']['NEW'].fillna(0).cumsum()
brand_pivot['cum_EXISTING'] = brand_pivot['Customer_Count']['EXISTING'].fillna(0).cumsum()

#Plotting trend to compare cum data of Existing vs New Customer_Count
brand_pivot[['cum_EXISTING', 'cum_NEW']].plot()


#QUESTION 4
#Making a copy of df
df_market_contri = df.copy()

#Adding a new column in dataframe (Marketing_Contribution)
df_market_contri["Marketing_Contribution"]=df_market_contri["Gross_Profit"]-df_market_contri["Marketing_Spend"]

#Summing Marketing_Contribution by Date
aggreagate_by_date = df_market_contri.groupby(["Date"]).sum()

#Plotting daily Marketing Contribution for all channels and customer type together
plt.plot(aggreagate_by_date.index, aggreagate_by_date['Marketing_Contribution'], color='blue', linewidth=4,label='first_month')

#Summing Marketing_Contribution by Date and Channel
aggreagate_by_channel = df_market_contri.groupby(["Date","Channel"])["Marketing_Contribution"].sum().reset_index()

#Multiplotting daily Marketing Contribution for all channels
fig, axes = plt.subplots(nrows=4, ncols=3)
aggreagate_by_channel[aggreagate_by_channel.Channel=='Brand']['Marketing_Contribution'].plot(ax = axes[0,0])
aggreagate_by_channel[aggreagate_by_channel.Channel=='Branded Search']['Marketing_Contribution'].plot(ax = axes[0,1])
aggreagate_by_channel[aggreagate_by_channel.Channel=='Direct']['Marketing_Contribution'].plot(ax = axes[0,2])
aggreagate_by_channel[aggreagate_by_channel.Channel=='Display']['Marketing_Contribution'].plot(ax = axes[1,0])
aggreagate_by_channel[aggreagate_by_channel.Channel=='Mail']['Marketing_Contribution'].plot(ax = axes[1,1])
aggreagate_by_channel[aggreagate_by_channel.Channel=='Organic Search']['Marketing_Contribution'].plot(ax = axes[1,2])
aggreagate_by_channel[aggreagate_by_channel.Channel=='Organic Social']['Marketing_Contribution'].plot(ax = axes[2,0])
aggreagate_by_channel[aggreagate_by_channel.Channel=='Others']['Marketing_Contribution'].plot(ax = axes[2,1])
aggreagate_by_channel[aggreagate_by_channel.Channel=='Paid Search']['Marketing_Contribution'].plot(ax = axes[2,2])
aggreagate_by_channel[aggreagate_by_channel.Channel=='Referral']['Marketing_Contribution'].plot(ax = axes[3,0])
aggreagate_by_channel[aggreagate_by_channel.Channel=='Unidentified']['Marketing_Contribution'].plot(ax = axes[3,1])


#Question 5
import numpy as np

#Creating dataframe from df that has Channel = Organic Search
organic_search=df[df.Channel=="Organic Search"].copy()

#Creating dataframe from df that has Channel = Paid Search
paid_search=df[df.Channel=="Paid Search"].copy()

#Removing all columns except for Revenue
organic_search_cols=organic_search[["Revenue"]]
paid_search_cols=paid_search[["Revenue"]]

#Summing Revenue by Date
organic_search_rev = organic_search_cols.groupby(["Date"], as_index=False)["Revenue"].sum()
paid_search_rev = paid_search_cols.groupby(["Date"], as_index=False)["Revenue"].sum()

#Finding PEARSON Correlation
np.corrcoef(organic_search_rev["Revenue"],paid_search_rev["Revenue"])

#Assigning ggplot as the style
plt.style.use('ggplot')

#Plotting a scatter plot to see if it is positive or negatively correlated
plt.scatter(organic_search_rev["Revenue"],paid_search_rev["Revenue"])
plt.show()



