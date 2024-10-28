import geopandas as gpd
from shapely.geometry import Point
import pandas as pd

# Load the zip code shapefile (ensure it's a spatial file with geometry)
zip_codes = gpd.read_file('/Users/hollandamazonia/Downloads/tl_2022_us_zcta520/tl_2022_us_zcta520.shp')

# Load your weather stations dataset (CSV, for example) and create a GeoDataFrame
stations_df = pd.read_csv('/Users/hollandamazonia/Downloads/merged_weather_lat_long.csv')

# Create a geometry column from the latitude and longitude of the stations
stations_gdf = gpd.GeoDataFrame(stations_df, 
                                geometry=gpd.points_from_xy(stations_df.longitude, stations_df.latitude),
                                crs="EPSG:4326")  # WGS84, commonly used for lat/lon
# Reproject the zip code shapefile to match the stations (if necessary)
if zip_codes.crs != stations_gdf.crs:
    zip_codes = zip_codes.to_crs(stations_gdf.crs)

# Perform spatial join
joined_gdf = gpd.sjoin(stations_gdf, zip_codes, how="left", op="within")
print(joined_gdf.head())

# Save to CSV
joined_gdf.drop(columns='geometry').to_csv('weather_stations_with_zip_codes.csv', index=False)

# Or save to a GeoJSON file if you want to keep the spatial information
# joined_gdf.to_file('weather_stations_with_zip_codes.geojson', driver='GeoJSON')

