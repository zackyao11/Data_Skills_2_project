#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 17:08:07 2020

@author: Mohamed
"""


import pandas as pd
import geopandas as gp
import PIL
import io
import pylab as plot
import os
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split 
from sklearn.naive_bayes import GaussianNB 
from sklearn import metrics 

# ---------- Mapping COVID cases Globally ----------------

# Load Johns Hopkins covid-19 data
covid_path = os.path.abspath(r'/Users/Mohamed/Documents/GitHub/Data_Skills_2_project/time_series_covid19_confirmed_global.csv')
covid_data = pd.read_csv(covid_path)

# Remove states/provinces and groupby country
covid_data = covid_data.groupby('Country/Region').sum()

# Load World shapefile
world_path = os.path.abspath(r'/Users/Mohamed/Documents/GitHub/Data_Skills_2_project/World_Countries__Generalized_-shp 2/World_Countries__Generalized_.shp')
world = gp.read_file(world_path)

#world = world.groupby()

# check for discrepencies between shapefile and covid csv
for index, row in covid_data.iterrows():
    if index not in world['COUNTRY'].to_list():
        print(index + ' is not included in shapefile')
    else:
        pass
    
world.replace('Taiwan', 'Taiwan*', inplace= True)
world.replace('Myanmar', 'Burma', inplace= True)
world.replace('Congo', 'Congo (Brazzaville)', inplace= True)
world.replace('Brunei Darussalam', 'Brunei', inplace= True)
world.replace('Congo DRC','Congo (Kinshasa)', inplace= True)
world.replace('Czech Republic', 'Czechia', inplace= True)
world.replace('CÃ´te d\'Ivoire','Cote d\'Ivoire', inplace= True)
world.replace('South Korea', 'Korea, South', inplace= True)
world.replace('Russian Federation','Russia', inplace= True)
world.replace('United States', 'US', inplace= True)
world.replace('Palestinian Territory', 'West Bank and Gaza', inplace= True)


# Merging World with covid data
merged_world = world.join(covid_data, on = 'COUNTRY', how = 'right')  
#merged_world.plot()


# Plotting a single date 
params = {'legend.fontsize': 30,
          'legend.handlelength': 2,
          'legend.loc': 'lower left',
          'legend.markerscale': 3,
          'legend.borderaxespad': .1}
plot.rcParams.update(params) 

# Plot
ax = merged_world.plot(column = '11/14/20',
                       cmap = 'BuPu',
                       figsize = (60,60),
                       legend = True,
                       scheme = 'user_defined',
                       classification_kwds = {'bins':[1000, 10000, 20000, 50000, 100000,200000,350000, 500000, 2000000, 5000000, 10000000, 20000000]},
                       edgecolor = 'grey',
                       vmin = 0,
                       vmax = 13,
                       linewidth = .2)

# Add title and remove axis
ax.set_title('Total Confirmed COVID-19 Cases ' + '11/14/20', fontdict =
             {'fontsize' : 45}, pad = 12)
ax.set_axis_off()

# Move legend
ax.get_legend().set_bbox_to_anchor((0.1, 0.2))



# Plotting into a GIF  (Commented out because it takes too long to run, but it generates the attached gif)

image_frames = []

params = {'legend.fontsize': 30,
          'legend.handlelength': 2,
          'legend.loc': 'lower left',
          'legend.markerscale': 3,
          'legend.borderaxespad': .1}
plot.rcParams.update(params) 

# Function to run through all dates to plot all and save as images 
for date in merged_world.columns.to_list()[19:300]:
# Plot
    ax = merged_world.plot(column = date,
                       cmap = 'BuPu',
                       figsize = (45,45),
                       legend = True,
                       scheme = 'user_defined',
                       classification_kwds = {'bins':[1000, 10000, 20000, 50000, 100000,200000,350000, 500000, 2000000, 5000000, 10000000, 20000000]},
                       edgecolor = 'grey',
                       vmin = 0,
                       vmax = 13,
                       linewidth = .2)

# add title and remove axis
    ax.set_title('Total Confirmed COVID-19 Cases ' + date, fontdict =
             {'fontsize' : 45}, pad = 12)
    ax.set_axis_off()

# Move legend
    ax.get_legend().set_bbox_to_anchor((0.1, 0.2))
    image = ax.get_figure()

# append images
    f = io.BytesIO()
    image.savefig(f, format = 'png', bbox_inches = 'tight')
    f.seek(0)
    image_frames.append(PIL.Image.open(f))

# Put info into a GIF file with file title
image_frames[0].save('COVID-19 WORLD6.gif', format = 'GIF',
                     append_images = image_frames[1:],
                     save_all = True, duration = 100,
                     loop = 3)
f.close()



# ----------- Mapping Covid Data in the United States, by County  -------------

us_covid_path = os.path.abspath(r'/Users/Mohamed/Documents/GitHub/Data_Skills_2_project/us-counties.csv')
us_map_path = os.path.abspath(r'/Users/Mohamed/Documents/GitHub/Data_Skills_2_project/cb_2018_us_county_500k/cb_2018_us_county_500k.shp')
us_map_path = os.path.abspath(r'/Users/Mohamed/Documents/GitHub/Data_Skills_2_project/USA_Counties-shp 2/USA_Counties.shp')
# Load us covid data by county
us_data = pd.read_csv(us_covid_path)

# Load US shapefile, seperated by counties
us = gp.read_file(us_map_path)

# Rename column
us = us.rename(columns = {'NAME':'county'})

# Sort both
us = us.sort_values(by = ['county'])
us_data = us_data.sort_values(by = ['county'])

# Merging and removing Hawaii + Alaska for plotting reasons
merged_us = pd.merge(us, us_data, on = ['county'])  
merged_us = merged_us.drop_duplicates(subset = 'geometry')
merged_us = merged_us[~merged_us.state.str.contains('Hawaii')]
merged_us = merged_us[~merged_us.state.str.contains('Alaska')]
#merged_us = merged_us[~merged_us.STATEFP.str.contains('02')]
merged_us = merged_us[~merged_us.STATE_NAME.str.contains('Alaska')]
merged_us = merged_us[~merged_us.STATE_NAME.str.contains('Hawaii')]
merged_us = merged_us[~merged_us.state.str.contains('Puerto Rico')]

# Set axis parameters
import pylab as plot
params = {'legend.fontsize': 30,
          'legend.handlelength': 2,
          'legend.loc': 'lower left',
          'legend.markerscale': 3,
          'legend.borderaxespad': .1}
plot.rcParams.update(params)

# Plot
ax = merged_us.plot(column = 'cases',
                    cmap = 'BuPu',
                    figsize = (40,50),
                    legend = True,
                    scheme = 'user_defined',
                    classification_kwds = {'bins':[10, 100,500, 1000,2000, 5000, 20000,50000, 100000, 2000000]},
                    edgecolor = 'grey',
                    vmin = 0,
                    vmax = 10,
                    linewidth = .2)

# Add title and remove axis
ax.set_title('Total COVID-19 Cases by County 12/04/20' , fontdict =
             {'fontsize' : 60}, pad = 12)

ax.set_axis_off()

# Move legend
ax.get_legend().set_bbox_to_anchor((0.2, 0.2))




# Find counties with highest death rates
merged_us['deathrate'] = merged_us['deaths']/merged_us['cases'] * 100

# Plot
params = {'legend.fontsize': 30,
          'legend.handlelength': 2,
          'legend.loc': 'best',
          'legend.markerscale': 3,
          'legend.borderaxespad': .1}
plot.rcParams.update(params)

ax = merged_us.plot(column = 'deathrate',
                    cmap = 'BuPu',
                    figsize = (50,50),
                    legend = True,
                    scheme = 'user_defined',
                    classification_kwds = {'bins':[.05,.1,.25,.5, .75, 1 ,1.25,1.5,1.75, 2, 2.25, 2.5, 2.75, 3, 3.25 ,3.5, 5, 10]},
                    edgecolor = 'grey',
                    vmin = 0,
                    vmax = 17,
                    linewidth = .2)

# Add title and remove axis
ax.set_title('COVID-19 Death Rate by County 12/04/20' , fontdict =
             {'fontsize' : 60}, pad = 12)

ax.set_axis_off()

# Move legend
ax.get_legend().set_bbox_to_anchor((1, 0.5))
merged_us['deathrate'].value_counts()



# ----  Testing if percentage of POC in a county contributes to higher death rates -----

# POC
merged_us['pocrate'] = (merged_us['POPULATION'] - merged_us['WHITE'])/merged_us['POPULATION'] * 100

# Plot
ax = merged_us.plot(column = 'pocrate',
                    cmap = 'BuPu',
                    figsize = (50,50),
                    legend = True,
                    scheme = 'user_defined',
                    classification_kwds = {'bins':[1,5,10,15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95]},
                    edgecolor = 'grey',
                    vmin = 0,
                    vmax = 19,
                    linewidth = .2)

# add title and remove axis
ax.set_title('Percentage POC by County 12/04/20' , fontdict =
             {'fontsize' : 60}, pad = 12)

ax.set_axis_off()

# Move legend
ax.get_legend().set_bbox_to_anchor((1, 0.5))
merged_us['pocrate'].value_counts()

# Testing if 'pocrate' has effect on 'deathrate'

# rate of poc relative to deathrate
poc_cor = merged_us['pocrate'].corr(merged_us['deathrate'])
print('The correlation rate between the rate of POC in a county and the covid death rate in that county is: ', poc_cor)



# --------------------- Numpy testing using supervised Machine Learning ----------------------

# Supervised model to see if cases per county can be predicted after training on dataset

# Naive Bayes
merged_us = merged_us.dropna()
# Set training(X) and test(Y) data
X = merged_us.drop(['state', 'county', 'date','cases', 'STATE_NAME', 'FIPS', 'CNTY_FIPS', 'STATE_FIPS', 'geometry'], axis = 1).values
Y = merged_us['cases'].values
  
# Split X and y into training and testing 
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.4, random_state=1) 
  
# Training the model on training set 
model = GaussianNB() 
model.fit(X_train, Y_train) 
  
# Making predictions on the testing set 
Y_pred = model.predict(X_test) 
Y_pred

# Accuracy test
print( 'The accuracy of this covid-rate prediction test is:' , metrics.accuracy_score(Y_test,Y_pred)*100)



# Testing on deaths to check for better accuracy

X = merged_us.drop(['state', 'county', 'date','deaths', 'STATE_NAME', 'FIPS', 'CNTY_FIPS', 'STATE_FIPS', 'geometry'], axis = 1).values
Y = merged_us['deaths'].values
  
# Split X and y into training and testing 
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.4, random_state=1) 
  
# Training the model on training set 
model = GaussianNB() 
model.fit(X_train, Y_train) 
  
# Making predictions on the testing set 
Y_pred = model.predict(X_test) 
Y_pred

# Accuracy test
print('The accuracy of this death-rate prediction test is:' ,metrics.accuracy_score(Y_test,Y_pred)*100)



# --------- WRITE-UP ------------


''' 
My project seeks to map Coronavirus cases in a way that is both informative and visually appealing. I have created both still maps and a 
gif file featuring dynamic mapping that I have attached (the gif file is best viewed on a web browser). I have included both global data and 
us-specific data in my mapping. The global data includes cases from February through mid November. Aside from the mapping, I have also set 
up a correlation test  to check for a correlation between the level of peopple of color in a county and the death rate in that county. 
I have also created a supervised machine-learning model in an attempt to predict cases per county after training the model on other demographic
 data points. 

'''