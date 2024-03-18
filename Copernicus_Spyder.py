# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 23:44:25 2024

@author: micha
"""

from IPython.display import IFrame
%matplotlib inline
import matplotlib.pyplot as plt
import pydap
import pandas as pd
import numpy as np
import math
import datetime
from datetime import timedelta
import os
import getpass
import xarray as xr
import panel.widgets as pnw
import panel as pn
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import copernicus_marine_client  as copernicus_marine

# To avoid warning messages
import warnings
warnings.filterwarnings('ignore')

class Coord:
    '''An improved class to represent lat/lon values.'''

    def __init__(self,lat,lon):
        self.lat = float(lat)  # make sure it's a float
        self.lon = float(lon)

    # Follows the specification described in the Aviation Formulary v1.46
    # by Ed Williams (originally at http://williams.best.vwh.net/avform.htm)
    def dist_to(self, other):
        lat1 = Coord.deg2rad(self.lat)
        lon1 = Coord.deg2rad(self.lon)
        lat2 = Coord.deg2rad(other.lat)
        lon2 = Coord.deg2rad(other.lon)

        # there are two implementations of this function.
        # implementation #1:
        #dist_rad = math.acos(math.sin(lat1) * math.sin(lat2)
        #                   + math.cos(lat1) * math.cos(lat2) * math.cos(lon1-lon2))

        # implementation #2: (less subject to numerical error for short distances)
        dist_rad=2*math.asin(math.sqrt((math.sin((lat1-lat2)/2))**2 +
                   math.cos(lat1)*math.cos(lat2)*(math.sin((lon1-lon2)/2))**2))

        return Coord.rad2nm(dist_rad)
    
    def __str__(self):
        return "(%f,%f)" % (self.lat,self.lon)

    def __repr__(self):
        return "Coord(%f,%f)" % (self.lat,self.lon)

    def deg2rad(degrees):
        '''Converts degrees (in decimal) to radians.'''
        return (math.pi/180)*degrees

    def rad2nm(radians):
        '''Converts a distance in radians to a distance in nautical miles.'''
        return ((180*60)/math.pi)*radians

# end of class Coord


## Product's parameter for GLOBAL_ANALYSISFORECAST_WAV_001_027 wave heights 
datasetID = 'cmems_mod_glo_wav_anfc_0.083deg_PT3H-i'
DS = copernicus_marine.open_dataset(dataset_id = datasetID)

subset_malacca = DS[['VHM0', 'VMDR', 'VCMX']].sel(longitude=slice(93,110),latitude=slice(-10,10))

#read in clean dataset
piracy_df = pd.read_csv('Data_Files\[Clean] IMO Piracy - 2000 to 2022 (PDV 01-2023).csv')
piracy_df_map = piracy_df.dropna(subset=['Latitude','Longitude']) #drop lat/long nulls: actually useful info on map
piracy_df_names = piracy_df_map.set_index('Ship Name')
piracy_df_names = piracy_df_names.rename(columns={"Incident Date": "Incident_Date"}, errors="raise") #doing this because i cant use .Incident_Date to call that column without renaming it 

#convert piracy_df_names incident dates to datetimes
piracy_df_names['Incident_Date'] = pd.to_datetime(piracy_df_names['Incident_Date'])

#first testing the time buffer for the specific instance, then putting it into a loop
#setting buffers so I have data that straddles the event in a 1x1 degree box lat/lon and 1 day (12 hours before 12 after)
time_buffer = pd.Timedelta(0.5, unit="h") #d "day", h "hour", m "minute"
lat_buffer = 0.05 #degree 
lon_buffer = 0.05 #degree

#set the lat and lon to the Buena Reina event
lat = piracy_df_names.loc['Magnum Energy'].Latitude
lon = piracy_df_names.loc['Magnum Energy'].Longitude
Coord_Magnum = Coord(lat,lon)
time = piracy_df_names.loc['Magnum Energy'].Incident_Date

#Use the buffer to make a subset of the weather data for points around the event
lat_add = lat + lat_buffer
lat_subtract = lat - lat_buffer
lon_add = lon + lon_buffer
lon_subtract = lon - lon_buffer
time_add = time + time_buffer
time_subtract = time - time_buffer

#create my data subset for the bubble around this specific piracy event
subset_Magnum_Energy = DS[['VHM0', 'VMDR', 'VCMX']].sel(
    latitude = slice(lat_subtract,lat_add),
    longitude = slice(lon_subtract,lon_add),
    time = slice(time_subtract, time_add)   )

print(subset_Magnum_Energy['VHM0'])