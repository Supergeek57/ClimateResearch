from striprtf.striprtf import rtf_to_text
import pandas as pd

# Step 1: Convert RTF to plain text
with open('/Users/hollandamazonia/Downloads/ghcnd_stations.rtf', 'r') as file:
    rtf_content = file.read()

plain_text = rtf_to_text(rtf_content)

# Step 2: Write the plain text to a temporary file (or parse directly)
with open('ghcnd_stations.txt', 'w') as txt_file:
    txt_file.write(plain_text)

# Step 3: Parse the plain text file with pandas using fixed-width columns
colspecs = [(0, 11),  # Station ID
            (12, 20),  # Latitude
            (21, 30),  # Longitude
            (31, 37),  # Elevation
            (38, 40),  # State
            (41, 71)]  # Station Name

col_names = ['station_id', 'latitude', 'longitude', 'elevation', 'state', 'station_name']

# Load the plain text into a pandas DataFrame
stations_df = pd.read_fwf('ghcnd_stations.txt', colspecs=colspecs, names=col_names)

# Convert latitude, longitude, and elevation to numeric types
stations_df['latitude'] = pd.to_numeric(stations_df['latitude'], errors='coerce')
stations_df['longitude'] = pd.to_numeric(stations_df['longitude'], errors='coerce')
stations_df['elevation'] = pd.to_numeric(stations_df['elevation'], errors='coerce')

# Save the DataFrame to CSV
stations_df.to_csv('ghcnd_stations.csv', index=False)

print(stations_df.head())
