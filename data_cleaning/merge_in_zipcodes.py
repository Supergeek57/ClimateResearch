import geopandas as gpd
from shapely.geometry import Point
import pandas as pd

# Load the zip code shapefile (ensure it's a spatial file with geometry)
print("Reading shapefile...")
zip_codes = gpd.read_file('/Users/hollandamazonia/Downloads/tl_2022_us_zcta520/tl_2022_us_zcta520.shp')
print("Done reading shapefile")

# Load your weather stations dataset (CSV, for example) and create a GeoDataFrame
print("Reading CSV...")
stations_df = pd.read_csv('/Users/hollandamazonia/Downloads/ghcnd_stations.csv')
print("Done reading CSV")

# Create a geometry column from the latitude and longitude of the stations
print("Creating GeoDataFrame...")
stations_gdf = gpd.GeoDataFrame(stations_df, 
                                geometry=gpd.points_from_xy(stations_df.longitude, stations_df.latitude),
                                crs="EPSG:4326")  # WGS84, commonly used for lat/lon
# Reproject the zip code shapefile to match the stations (if necessary)
if zip_codes.crs != stations_gdf.crs:
    zip_codes = zip_codes.to_crs(stations_gdf.crs)
print("Done")

# Perform spatial join
print("Performing spatial join...")
joined_gdf = gpd.sjoin(stations_gdf, zip_codes, how="left", predicate="within")
print(joined_gdf.head())
print("Done")

# Save to CSV
print("Saving to CSV...")
joined_gdf.drop(columns='geometry').to_csv('all_stations_with_zip.csv', index=False)
print("Done")
# Or save to a GeoJSON file if you want to keep the spatial information
# joined_gdf.to_file('weather_stations_with_zip_codes.geojson', driver='GeoJSON')

