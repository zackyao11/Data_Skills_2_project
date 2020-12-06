import pandas_datareader.data as web
import datetime
import pandas as pd

start = datetime.datetime(2019,10,1)
end = datetime.datetime(2020,12,1)
savings = web.DataReader('PSAVERT','fred',start,end) #personal saving rate changes
SP500 = web.DataReader('SP500','fred',start,end) #S&P 500 changes
jbopen = web.DataReader('JTS1000JOL','fred',start,end) #job opening for private changes 
unemp = web.DataReader('UNRATE','fred',start,end) #unemployment rate changes
unemp_woman = web.DataReader('LNS14000002','fred',start,end) #unemployment rate for woman
unemp_man = web.DataReader('LNS14000001','fred',start,end) #unemployment rate for man
unemp_bl = web.DataReader('LNS14000006','fred',start,end) #unemployment rate for African American
unemp_wh = web.DataReader('LNS14000002','fred',start,end) #unemployment rate for White 
unemp_hi = web.DataReader('LNS14000009','fred',start,end) #unemployment rate for Hispanic
unemp_as = web.DataReader('LNU04032183','fred',start,end) #unemployment rate for Asian

savings.columns.values[0] = "Personal Saving Rate"
# source: https://stackoverflow.com/questions/20868394/changing-a-specific-column-name-in-pandas-dataframe
savings
df.columns.name = "year"
SP500 = SP500.resample('MS').mean()
# source: https://stackoverflow.com/questions/40554396/python-summarize-daily-data-in-dataframe-to-monthly-and-quarterly
jbopen
unemp
unemp_woman
unemp_man
unemp_bl
unemp_wh