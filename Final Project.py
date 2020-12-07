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
import numpy as np
warnings.simplefilter(action='ignore', category=FutureWarning)


path = r'/Users/suxinyun/Documents/GitHub/Data_Skills_2_project/'

# download data from fred
start = datetime.datetime(2019,10,1)
end = datetime.datetime(2020,9,1)
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

# make SP500 from daily data to monthly data
SP500 = SP500.resample('MS').mean()
# source: https://stackoverflow.com/questions/40554396/python-summarize-daily-data-in-dataframe-to-monthly-and-quarterly

#merge data
data_frames = [savings, SP500, jbopen, unemp, unemp_woman, unemp_man, unemp_wh, unemp_bl, unemp_hi, unemp_as]
merged = reduce(lambda left,right: pd.merge(left,right,on=['DATE'], how='outer'), data_frames)
merged = merged.reset_index()

#check if there is already an existing file in the path, if not, save the data
def check_exist(df, filename):
    if not os.path.exists(filename):
        df.to_csv(os.path.join(path, filename)) 

check_exist(merged,'Dataframe.csv')

# change the datetime data(e.g.2019-10-01) to only month(October)

def extract_datetime(df):
    row_list =[]
    for index, rows in df.iterrows(): 
        dates = [rows.DATE]
        row_list.append(dates[0])
    return row_list
row_list = extract_datetime(merged)

def create_month(row):
    month = []
    for date in row:
        date = time.strptime(str(date), "%Y-%m-%d %H:%M:%S")
        monthname = calendar.month_name[date.tm_mon]
        month.append(monthname)
    return month
month = create_month(row_list)

def date_to_month(df):
    df1 = df.set_index('DATE')
    for i in range(len(df['DATE'])):
        df1 = df1.rename({row_list[i]: month[i]}, axis = 0)
    return df1
merged1 = date_to_month(merged)

check_exist(merged1,'Dataframe Revised.csv')

# source: https://stackoverflow.com/questions/6556581/convert-date-to-months-and-year
# source: https://stackoverflow.com/questions/55941595/how-to-convert-timestamp-into-string-in-python
# source: https://www.geeksforgeeks.org/create-a-list-from-rows-in-pandas-dataframe/
# source: https://stackoverflow.com/questions/3743222/how-do-i-convert-a-datetime-to-date


# create a plot for gender and unemployment rate
gender_col = ["DATE", "Unemp Rate", "Unemp Rate_Male", "Unemp Rate_Female"]
def merge_data(df, col, var_name):
    '''
    reset index and stack dataframe for plot
    '''
    df1 = df.reset_index()
    df1 = df1[col].dropna()
    df1 = df1.set_index('DATE').stack()
    df1 = pd.DataFrame(df1).reset_index()
    df1 = df1.rename(columns={'level_1':var_name,0:'unemp rate'})
    return df1
gender = merge_data(merged1,gender_col, 'gender')

# create a barplot for gender dataframe
def create_bar(df):
    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(10,7), dpi = 200)
    
    sns.barplot('DATE', 'unemp rate', hue='gender',data=df, color='slateblue',ci=0)
    legend = ax.legend()
    legend.texts[0].set_text("all")
    legend.texts[1].set_text("male")
    legend.texts[2].set_text("female")
    plt.title('Unemployment Rate from October 2019 to September 2020', loc='Center', fontsize=14)
    plt.ylabel('Unemployment Rate')
    plt.xlabel('Month')
    plt.xticks(rotation=30, fontsize=8)
    if not os.path.exists('unemployment rate by gender.png'):
        plt.savefig(os.path.join(path, 'unemployment rate by gender.png'))

create_bar(gender)

# source: https://stackoverflow.com/questions/6390393/matplotlib-make-tick-labels-font-size-smaller
# source: https://stackoverflow.com/questions/51579215/remove-seaborn-lineplot-legend-title

# stack merged1 dataframe to plot the unemployment by race
race_col = ["DATE", "Unemp Rate", "Unemp Rate_White", "Unemp Rate_Black","Unemp Rate_Hispanic","Unemp Rate_Asian"]
race = merge_data(merged1, race_col, 'race')

# create lineplot for unemployment by race
def create_line(df):
    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(10,7), dpi = 200)
    
    sns.lineplot('DATE', 'unemp rate', hue='race',data=df, marker = 'o', color='olive',ci=0)
    legend = ax.legend()
    legend.texts[0].set_text("All")
    legend.texts[1].set_text("White")
    legend.texts[2].set_text("African American")
    legend.texts[3].set_text("Hispanic")
    legend.texts[4].set_text("Asian")
    plt.title('Unemployment Rate from October 2019 to September 2020', loc='Center', fontsize=14)
    plt.ylabel('Unemployment Rate')
    plt.xlabel('Month')
    plt.xticks(rotation=30, fontsize=8)
    if not os.path.exists('unemployment rate by gender.png'):
        plt.savefig(os.path.join(path, 'unemployment rate by race.png'))
create_line(race)

#create a new dataframe for plotting in jupyter notebook
#generate a new column "waves" to suggest for different waves for the pandemic
merged['DATE']=merged['DATE'].astype(str)

precorona = ['2019-10-01','2019-11-01','2019-12-01','2020-01-01','2020-02-01']
firstwave = ['2020-03-01', '2020-04-01','2020-05-01', '2020-06-01']

def label_wave(row):
   if row['DATE'] in (precorona):
       return 'Pre-Corona'
   if row['DATE'] in (firstwave):
       return 'First Wave'
   return 'Second Wave'

merged['Covid Wave'] = merged.apply(lambda row: label_wave(row), axis=1)
merged['DATE'] = pd.to_datetime(merged['DATE'])

# source: https://stackoverflow.com/questions/61118221/python-apply-custom-function-to-string-columns-does-not-work
# source: https://stackoverflow.com/questions/26886653/pandas-create-new-column-based-on-values-from-other-columns-apply-a-function-o

# change the datetime data(e.g.2019-10-01) to only month(October)
row_list = extract_datetime(merged)
month = create_month(row_list)
merged2 = date_to_month(merged)
merged2 = merged2.reset_index()

check_exist(merged2,'Complete Dataframe.csv')

#create a plot for plotting 
wave = ['Pre-Corona','First Wave', 'Second Wave']
def clean_data(df):
    df['DATE'] = df['DATE'].astype(str)
    df1 = df[['DATE','Covid Wave','Unemp Rate']]
    df1 = df1.set_index(['DATE','Covid Wave'])
    df1 = df1.unstack().reindex(df1.index.get_level_values(0))
    df1.columns = df1.columns.droplevel(0)
    df1 = df1[wave]
    df1 = df1.reset_index()
    return df1
unemp_wave = clean_data(merged2)

# save the data for interactive plots
check_exist(unemp_wave,'Dataframe for Plotting.csv')




