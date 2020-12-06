import pandas_datareader.data as web
import datetime
import pandas as pd
import calendar
from functools import reduce
import os
import time
import warnings
import seaborn as sns
import matplotlib.pyplot as plt
warnings.simplefilter(action='ignore', category=FutureWarning)


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
unemp = load_data('UNRATE', 'Unemp Rate') #unemployment rate changes
unemp_woman = load_data( 'LNS14000002', "Unemp Rate_Female") #unemployment rate for woman
unemp_man = load_data('LNS14000001', 'Unemp Rate_Male') #unemployment rate for man
unemp_bl = load_data('LNS14000006', 'Unemp Rate_Black')#unemployment rate for African American
unemp_wh = load_data('LNS14000002', 'Unemp Rate_White') #unemployment rate for White 
unemp_hi = load_data( 'LNS14000009', 'Unemp Rate_Hispanic') #unemployment rate for Hispanic
unemp_as = load_data('LNU04032183','Unemp Rate_Asian') #unemployment rate for Asian

def time_data(category, colname, start, end):
    df = web.DataReader(category, 'fred', start, end)
    df.columns.values[0] = colname
    return df
start1 = datetime.datetime(2008, 1, 1)
start2 = datetime.datetime(2019,1,1)
end1 = datetime.datetime(2009,1,1)
end2 = datetime.datetime(2020,1,1)
ecocrisis = time_data('UNRATE', 'Unemp Rate', start1, end1) #unemployment rate in economic crisis in 2008
precorona = time_data('UNRATE', 'Unemp Rate', start2, end2) #unemployment rate in precorona period

SP500 = SP500.resample('MS').mean()
# source: https://stackoverflow.com/questions/40554396/python-summarize-daily-data-in-dataframe-to-monthly-and-quarterly

data_frames = [savings, SP500, jbopen, unemp, unemp_woman, unemp_man, unemp_wh, unemp_bl, unemp_hi, unemp_as]
merged = reduce(lambda left,right: pd.merge(left,right,on=['DATE'], how='outer'), data_frames)
merged = merged.reset_index()

merged 

#### add an if condition
merged.to_csv(os.path.join(path, "Final Dataframe.csv")) 



ecocrisis
precorona


row_list =[]
for index, rows in merged.iterrows(): 
        dates = [rows.DATE]
        row_list.append(dates[0])


row_list

month = []
for date in row_list:
    date = time.strptime(str(date), "%Y-%m-%d %H:%M:%S")
    monthname = calendar.month_name[date.tm_mon]
    month.append(monthname)

month

merged1 = merged.set_index('DATE')
for i in range(len(merged['DATE'])):
    merged1 = merged1.rename({row_list[i]: month[i]}, axis = 0)


merged1 = merged1.reset_index()
merged1

# source: https://stackoverflow.com/questions/6556581/convert-date-to-months-and-year
# source: https://stackoverflow.com/questions/55941595/how-to-convert-timestamp-into-string-in-python
# source: https://www.geeksforgeeks.org/create-a-list-from-rows-in-pandas-dataframe/
# source: https://stackoverflow.com/questions/3743222/how-do-i-convert-a-datetime-to-date
gender = merged1[["DATE", "Unemp Rate", "Unemp Rate_Male", "Unemp Rate_Female"]].dropna()
gender = gender.set_index('DATE').stack()
gender = pd.DataFrame(gender).reset_index()
gender
gender = gender.rename(columns={'level_1':'gender',0:'unemp rate'})

plt.style.use('ggplot')
fig, ax = plt.subplots(figsize=(10,7), dpi = 200)

sns.barplot('DATE', 'unemp rate', hue='gender',data=gender, color='slateblue',ci=0)
legend = ax.legend()
legend.texts[0].set_text("all")
legend.texts[1].set_text("male")
legend.texts[2].set_text("female")
plt.title('Unemployment Rate from October 2019 to November 2020', loc='Center', fontsize=14)
plt.ylabel('Unemployment Rate')
plt.xlabel('Month')
plt.xticks(rotation=30, fontsize=8)
plt.savefig(os.path.join(path, 'unemployment rate for men and women.png'))

# source: https://stackoverflow.com/questions/6390393/matplotlib-make-tick-labels-font-size-smaller






# def date_to_month(df):
#     for index, rows in df.iterrows(): 
#         dates = [rows.DATE]
#         Row_list.append(dates) 

#     for date in row_list:
#         date = time.strptime(str(date[0]), "%Y-%m-%d %H:%M:%S")
#         calendar.month_name[date.tm_mon]

#     for i in range(len(df['DATE'])):
#         df = df.rename({Row_list[i]: month[i]}, axis = 0)


### datetime.date()