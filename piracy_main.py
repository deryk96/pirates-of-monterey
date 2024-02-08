"""
This is the main file required for the Piracy Data Analysis project in Computational Methods II.
We.are.pirates. Bum-ba-dum, dum-dum-dum-dum.
"""

__author__ = "Deryk Clary, Julia MacDonald, Michael Galvan, and MaryGrace Burke"
__credits__ = ["Deryk Clary", "Julia Macdonald", "Michael Galvan", "MaryGrace Burke"]
__email__ = ["deryk.clary@nps.edu", "julia.macdonald@np.edu"]  # TODO Add emails
__status__ = "Development"

# Import Libraries
from piracy_classes import build_vessel_dict
import geopandas as gpd
from shapely.geometry import Point, Polygon
import pandas as pd
from pyproj import CRS
import matplotlib.pyplot as plt


def build_map(data_dict, data_path):
    """ Builds a map from a dictionary of vessels with piracy incidents. Saves the map to disk in .jpg format and
    displays the map in the console.
    -Code snippets borrowed from the article by Ian Forrest on 20240124
    -Link: https://medium.com/@ianforrest11/graphing-latitudes-and-longitudes-on-a-map-bf64d5fca391
    """

    # Open CSV (TODO need to figure out how to read all data out of the dictionary instead, if possible)
    df = pd.read_csv(data_path)

    # Get lats and longs
    lats = []
    lons = []
    for vessel in data_dict:
        vessel_incidents = data_dict[vessel].get_incidents()
        for incident in vessel_incidents:
            if vessel_incidents[incident].coord is not None:
                lats.append(vessel_incidents[incident].coord.lat)
                lons.append(vessel_incidents[incident].coord.lon)
            else:
                # TODO Figure out a better way to ignore null values.
                lats.append('0')
                lons.append('0')

    # Import the countries map
    # street_map = gpd.read_file('Data_Files/ne_10m_populated_places_map/ne_10m_populated_places.shp')
    # street_map = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
    street_map = gpd.read_file('https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_110m_land.geojson')

    # Designate the coordinate system
    crs = CRS("EPSG:4326")

    # Set font to helvetica
    hfont = {'fontname': 'Helvetica'}

    # Zip x and y coordinates into single feature
    geometry = [Point(xy) for xy in zip(lons, lats)]

    # create GeoPandas dataframe
    geo_df = gpd.GeoDataFrame(df, crs=crs, geometry=geometry)

    # Create figure and axes, assign to subplot
    fig, ax = plt.subplots(figsize=(15, 15))

    # Add .shp mapfile to axes
    street_map.plot(ax=ax, kind='geo', alpha=1, color='grey', edgecolor='grey', linewidth=1)

    geo_df.plot(ax=ax, color='red', markersize=7)

    # Add title / credit
    ax.annotate("Data: Incidents of Maritime Piracy, as reported to the International Maritime Organization of the UN, "
                "from 2000 to 2022. Accessed 24 Jan 24.\n"
                "https://data.world/project-data-viz/imo-piracy-2000-to-2022-pdv-01-2023a",
                **hfont, xy=(0.065, 0.13), xycoords='figure fraction', fontsize=10, color='#555555')
    ax.set_title("Incidents of Maritime Piracy",
                 **hfont, fontdict={'fontsize': '20', 'fontweight': '1'})

    # show map in console
    plt.show()

    # Save map to files
    fig.savefig('piracy.jpg', dpi=1080, bbox_inches='tight')
# End build_map

## Begin main portion

# Build dictionary from csv
path = 'Data_Files/IMO Piracy - 2000 to 2022 (PDV 01-2023).csv'
vessel_dict = build_vessel_dict(path)

# Build map of incidents in the console
build_map(vessel_dict, path)
# %%
