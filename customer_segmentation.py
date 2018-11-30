import pandas as pd
import warnings
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
color = sns.color_palette()
# For plotting and visualization:
from IPython.display import display
warnings.filterwarnings('ignore')
desired_width = 320
pd.set_option("display.max_columns", 10)
df = pd.read_excel("Online Retail.xlsx")
display(df.head())

# keep a copy as a backup.
df1 = df

#sanitity check about the data
df1.Country.nunique()
df1.Country.unique()

customer_country=df1[['Country','CustomerID']].drop_duplicates()

customer_country.groupby(['Country'])['CustomerID'].aggregate('count').reset_index().sort_values('CustomerID', ascending=False)

#some research indicating that customer clusters vary by geography,
#so here I’ll restrict the data to United Kingdom only.

df1 = df1.loc[df1['Country'] == 'United Kingdom']

#Executing some cleaning on data and checking their validity

df1.isnull().sum(axis=0)
#There are 133600 missing values in CustomerID column, since our analysis is based on customers,
#we will remove these missing values.

df1.isnull().sum(axis=0)
df1 = df1[pd.notnull(df1['CustomerID'])]
df1.isnull().sum(axis=0)

#Plotting the count of customers
country=list(customer_country['Country'])
Cust_id=list(customer_country['CustomerID'])
plt.figure(figsize=(12,8))
sns.barplot(country, Cust_id, alpha=0.8, color=color[2])
plt.xticks(rotation='60')
plt.show()

# # Check the min and max values in Unit price column and remove the negative values in Quantity column
#
# # df1.UnitPrice.min()
# # df1.Quantity.min()
#
#removing negative qties

df1 = df1[(df1['Quantity']>0)]
# # df1.Quantity.min()
#
# After cleaning up, we now dealing with 354345 rows and 8 columns
df1.shape
df1.info()
#
# Check unique value for each column

def unique_counts(df1):
    for i in df1.columns:
        count = df1[i].nunique()
        print(i, ": ", count)
unique_counts(df1)

# df1.head()
#
# Add a column for total

df1['TotalPrice'] = df1['Quantity'] * df1['UnitPrice']
# df1.head()
#
# #Find out first and last order date in the
df1['InvoiceDate'].min()

df1['InvoiceDate'].max()
#
#Since recency is calculated for a point in time.
#The last invoice date is 2011-12-09, this is the date we will use to calculate recency.


import datetime as dt
NOW = dt.datetime(2011,12,10)

df1['InvoiceDate'] = pd.to_datetime(df1['InvoiceDate'])

# #Create a RFM table
#
#
# rfmTable = df1.groupby('CustomerID').agg({'InvoiceDate': lambda x: (NOW - x.max()).days, # Recency
#                                           'InvoiceNo': lambda x: len(x),      # Frequency
#                                           'TotalPrice': lambda x: x.sum()}) # Monetary Value
#
# rfmTable['InvoiceDate'] = rfmTable['InvoiceDate'].astype(int)
# rfmTable.rename(columns={'InvoiceDate': 'recency',
#                          'InvoiceNo': 'frequency',
#                          'TotalPrice': 'monetary_value'}, inplace=True)
#
#
# #Calculate RFM metrics for each customer
#
# display(rfmTable.head())
#
# # Interpretation:
# # CustomerID 12346 has frequency:1, monetary value:$77183.60 and recency:324 days.
# # CustomerID 12747 has frequency: 103, monetary value: $4196.01 and recency: 1 day
# # Let's check the details of the first customer.
#
# first_customer = df1[df1['CustomerID']== 12346.0]
# first_customer
#
# #The first customer has shopped only once, bought one item at a huge quantity(74215).
# #The unit price is very low, seems a clearanceT sale.
#
# (NOW - dt.datetime(2011,1,18)).days==326
#
# #The easiest way to split metrics into segments is by using quartile :
# #This gives us a starting point for detailed analysis
# #4 segments are easy to understand and explain
#
# quantiles = rfmTable.quantile(q=[0.25,0.5,0.75])
# quantiles
#
# quantiles = quantiles.to_dict()
# quantiles
#
# #Create a segmented RFM table
#
# segmented_rfm = rfmTable
#
# #Lowest recency, highest frequency and monetary are our best customers
#
# def RScore(x,p,d):
#     if x <= d[p][0.25]:
#         return 1
#     elif x <= d[p][0.50]:
#         return 2
#     elif x <= d[p][0.75]:
#         return 3
#     else:
#         return 4
#
# def FMScore(x,p,d):
#     if x <= d[p][0.25]:
#         return 4
#     elif x <= d[p][0.50]:
#         return 3
#     elif x <= d[p][0.75]:
#         return 2
#     else:
#         return 1
#
# segmented_rfm['r_quartile'] = segmented_rfm['recency'].apply(RScore, args=('recency',quantiles,))
# segmented_rfm['f_quartile'] = segmented_rfm['frequency'].apply(FMScore, args=('frequency',quantiles,))
# segmented_rfm['m_quartile'] = segmented_rfm['monetary_value'].apply(FMScore, args=('monetary_value',quantiles,))
#
# #Add segment numbers to the RFM table
#
# segmented_rfm.head()
#
# #RFM segments split your customer base into an imaginary 3D cube. It is hard to visualize. However, we can sort it out.
# #Add a new column to combine RFM score, 111 is the highest score as we determined earlier.
#
# segmented_rfm['RFMScore'] = segmented_rfm.r_quartile.map(str) \
#                             + segmented_rfm.f_quartile.map(str) \
#                             + segmented_rfm.m_quartile.map(str)
# segmented_rfm.head()
#
# #Apparently, the first customer is not our best customer at all.
#
# #Here is top 10 of our best customers!
#
# segmented_rfm[segmented_rfm['RFMScore']=='111'].sort_values('monetary_value', ascending=False).head(10)
#
#
#
