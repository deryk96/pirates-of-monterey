"""
This is the main file required for the Piracy Data Analysis project in Computational Methods II.
We.are.pirates. Bum-ba-dum, dum-dum-dum-dum.
"""

__author__ = "Deryk Clary, Julia MacDonald, Michael Galvan, and MaryGrace Burke"
__credits__ = ["Deryk Clary", "Julia Macdonald", "Michael Galvan", "MaryGrace Burke"]
__email__ = ["deryk.clary@nps.edu", "ADD OTHERS"]
__status__ = "Development"

# Import Libraries
from piracy_classes import build_vessel_dict
import geopandas as gpd
from shapely.geometry import Point, Polygon
import pandas as pd
import matplotlib.pyplot as plt

vessel_dict = build_vessel_dict('Data_Files/IMO Piracy - 2000 to 2022 (PDV 01-2023).csv')

# Map out all the incidents
# Code borrowed from the Internet on 20240124
# Link: https://medium.com/@ianforrest11/graphing-latitudes-and-longitudes-on-a-map-bf64d5fca391
# Open CSV (TODO need to figure out how to read all data out of the dictionary instead)
df = pd.read_csv('Data_Files/IMO Piracy - 2000 to 2022 (PDV 01-2023).csv')

# Get lats and longs
lats = []
lons = []
for vessel in vessel_dict:
    for incident in vessel_dict[vessel].incidents:
        if vessel_dict[vessel].incidents[incident].coord is not None:
            lats.append(vessel_dict[vessel].incidents[incident].coord.lat)
            lons.append(vessel_dict[vessel].incidents[incident].coord.lon)

# Import the countries map
# TODO Figure out why this file isn't being read in
street_map = gpd.read_file('Data_Files/ne_10m_populated_places_map/ne_10m_populated_places.shp')
# street_map = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

# Designate the coordinate system
crs = {'init': 'epsg:4326'}

# Zip x and y coordinates into single feature
geometry = [Point(xy) for xy in zip(lats, lons)]

# create GeoPandas dataframe
geo_df = gpd.GeoDataFrame(df, crs=crs, geometry=geometry)

# Create figure and axes, assign to subplot
fig, ax = plt.subplots(figsize=(15, 15))

# Add .shp mapfile to axes
street_map.plot(ax=ax, alpha=1, color='grey', linewidth=1)

geo_df.plot(ax=ax, color='red', markersize=10)

fig.suptitle('Plot of Piracy Incidents', fontsize=12)

# show map
plt.show()
