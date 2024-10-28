import csv
from datetime import datetime

# Function to check if a station's date range covers 2019
def has_data_in_2019(min_date, max_date):
    start_2019 = datetime(2019, 1, 1)
    end_2019 = datetime(2019, 12, 31)
    min_date = datetime.strptime(min_date, '%Y-%m-%d')
    max_date = datetime.strptime(max_date, '%Y-%m-%d')
    
    # Check if the station's date range includes any part of 2019
    return max_date >= start_2019 and min_date <= end_2019

# Open the original CSV file with all stations
with open('us_weather_stations.csv', 'r') as infile, open('stations_with_data_2019.csv', 'w', newline='') as outfile:
    reader = csv.DictReader(infile)
    writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
    writer.writeheader()

    # Loop through each station in the original file
    for row in reader:
        station_id = row['Station ID']
        min_date = row['Min Date']
        max_date = row['Max Date']

        # Check if the station has data that covers any part of 2019
        if has_data_in_2019(min_date, max_date):
            writer.writerow(row)  # Write the station info to the new file
            print(f"Station {station_id} has data from 2019.")
        else:
            print(f"Station {station_id} does not have data from 2019.")

print("Filtered list of stations with data from 2019 has been saved to 'stations_with_data_2019.csv'.")
