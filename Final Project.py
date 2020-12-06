import pandas_datareader.data as web
import datetime
import pandas as pd
import calendar
from functools import reduce
import os

path = r'/Users/suxinyun/Documents/GitHub/Data_Skills_2_project/'

start = datetime.datetime(2019,10,1)
end = datetime.datetime(2020,12,1)
def load_data(category, colname):
    df = web.DataReader(category, 'fred', start, end)
    df.columns.values[0] = colname
    return df
# source: https://stackoverflow.com/questions/20868394/changing-a-specific-column-name-in-pandas-dataframe

savings = load_data('PSAVERT', 'Personal Saving Rate')#personal saving rate changes
SP500 = load_data('SP500', "S&P 500")#S&P 500 changes
jbopen = load_data('JTS1000JOL', 'Job Openings')#job opening for private changes 
unemp = load_data( 'UNRATE', 'Unemp Rate') #unemployment rate changes
unemp_woman = load_data( 'LNS14000002', "Unemp Rate_Female") #unemployment rate for woman
unemp_man = load_data('LNS14000001', 'Unemp Rate_Male') #unemployment rate for man
unemp_bl = load_data('LNS14000006', 'Unemp Rate_Black')#unemployment rate for African American
unemp_wh = load_data('LNS14000002', 'Unemp Rate_White') #unemployment rate for White 
unemp_hi = load_data( 'LNS14000009', 'Unemp Rate_Hispanic') #unemployment rate for Hispanic
unemp_as = load_data('LNU04032183','Unemp Rate_Asian') #unemployment rate for Asian


SP500 = SP500.resample('MS').mean()
# source: https://stackoverflow.com/questions/40554396/python-summarize-daily-data-in-dataframe-to-monthly-and-quarterly

data_frames = [savings, SP500, jbopen, unemp, unemp_woman, unemp_man, unemp_wh, unemp_bl, unemp_hi, unemp_as]
merged = reduce(lambda left,right: pd.merge(left,right,on=['DATE'], how='outer'), data_frames)
merged.to_csv(os.path.join(path, "Final Dataframe.csv"))
