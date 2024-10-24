import geopandas as gpd
from shapely.geometry import Point

# Load the zip code shapefile (ensure it's a spatial file with geometry)
zip_codes = gpd.read_file('path_to_zipcode_shapefile.shp')

# Load your weather stations dataset (CSV, for example) and create a GeoDataFrame
import pandas as pd
stations_df = pd.read_csv('weather_stations.csv')

# Create a geometry column from the latitude and longitude of the stations
stations_gdf = gpd.GeoDataFrame(stations_df, 
                                geometry=gpd.points_from_xy(stations_df.longitude, stations_df.latitude),
                                crs="EPSG:4326")  # WGS84, commonly used for lat/lon
