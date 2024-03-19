# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 23:44:25 2024
This file reads data from the Copernicus Marine API website and loads wave data for each individual
piracy event. 
@author: micha
"""
#!pip install copernicusmarine
#!pip install netCDF4
from IPython.display import IFrame
%matplotlib inline
import matplotlib.pyplot as pltmm
import pydap
import pandas as pd
import numpy as np
import math
import datetime
from datetime import timedelta
import xarray as xr

#import copernicus_marine_client  as copernicus_marine
import copernicusmarine  as copernicus_marine
# To avoid warning messages
import warnings
warnings.filterwarnings('ignore')

#Functions
def get_wave_height(row):
    if row['Incident Date'] >= DS_start_date:
        #print(row['Incident_Date'])
        lat = row['Latitude']
        lon = row['Longitude']
        Ship_Coord = Coord(lat, lon)
        #Ship_Coord_dict[row['Ship_Name']] = Ship_Coord
        
        #Use the buffer to make a subset of the weather data for points around the event
        lat_add = lat + lat_buffer
        lat_subtract = lat - lat_buffer
        lon_add = lon + lon_buffer
        lon_subtract = lon - lon_buffer
        time = row['Incident Date']
        time_add = time + time_buffer
        time_subtract = time - time_buffer
        
        #create my data subset for the bubble around this specific piracy event for wave height
        #hopefully this is only going to return one value for each point but it may return more or none
        subset = DS[['VHM0', 'VMDR', 'VCMX']].sel(
            latitude = slice(lat_subtract,lat_add),
            longitude = slice(lon_subtract,lon_add),
            time = slice(time_subtract, time_add))
        
        return subset['VHM0'].values[0][0]
#end of Functions


## Product's parameter for GLOBAL_ANALYSISFORECAST_WAV_001_027 wave heights 
datasetID = 'cmems_mod_glo_wav_anfc_0.083deg_PT3H-i'

#Use following username and password to load the dataset from Copernicus Marine Data Store
#Username: mgalvan
#Passwrd: 27OviedoSpain
DS = copernicus_marine.open_dataset(dataset_id = datasetID)

#read in "clean" dataset
piracy_df = pd.read_csv('Data_Files\[Clean] IMO Piracy - 2000 to 2022 (PDV 01-2023).csv')

#create all dataframe organizaitons I'll need. 
piracy_df_map = piracy_df.dropna(subset=['Latitude','Longitude']) #drop lat/long nulls: actually useful info on map

#convert piracy_df_map incident dates to datetimes
piracy_df_map['Incident Date'] = pd.to_datetime(piracy_df_map['Incident Date'])
#piracy_df_map = piracy_df_map.rename(columns={"Ship Name": "Ship_Name","Incident Date": "Incident_Date"}, errors="raise")


#first testing the time buffer for the specific instance, then putting it into a loop
#setting buffers so I have data that straddles the event in a 1x1 degree box lat/lon and 1 day (12 hours before 12 after)
time_buffer = pd.Timedelta(0.5, unit="h") #d "day", h "hour", m "minute"
lat_buffer = 0.05 #degree 
lon_buffer = 0.05 #degree

#For this case with the wave data from 30 Sep 2021 to 25 Mar 2024 
DS_start_date = datetime.date(2021,9,30)
DS_end_date = datetime.date(2024,3,25)

#write code to augment this data to the new matrix 
piracy_df_map["Wave Height"] = piracy_df_map.apply(get_wave_height, axis=1)

#Show just the entries that have been augmented with not- NA values 
df_out = piracy_df_map[piracy_df_map["Wave Height"].notna()]
#write this dataframe to a csv
df_out.to_csv('piracy_df_waves1.csv', index=False) 