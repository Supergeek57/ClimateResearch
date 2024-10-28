import requests
import csv
import time

# NOAA API token
api_token = 'lOOvrVZobgoKOHZTPLgdnvivcLvutwjg'
headers = {'token': api_token}

# Base URL for NOAA CDO API
base_url = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/data'

# Parameters for checking if a station has data in 2019
data_params = {
    'datasetid': 'GHCND',
    'startdate': '2019-01-01',
    'enddate': '2019-12-31',
    'limit': 1  # We're just checking if any data exists, so limit to 1 result
}

# Function to check if a station has data in 2019
def has_2019_data(station_id):
    try:
        params = {**data_params, 'stationid': f'GHCND:{station_id}'}
        response = requests.get(base_url, headers=headers, params=params)
        data = response.json().get('results', [])
        return bool(data)  # Returns True if any data exists, False otherwise
    except requests.exceptions.RequestException as e:
        print(f"Error checking data for station {station_id}: {e}")
        return False

# Function to fetch full data for a station
def get_station_data(station_id):
    offset = 1
    station_data = []
    while True:
        params = {**data_params, 'stationid': f'GHCND:{station_id}', 'offset': offset, 'limit': 1000}
        try:
            response = requests.get(base_url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json().get('results', [])
            if not data:
                break
            for entry in data:
                entry['station_id'] = station_id
            station_data.extend(data)
            offset += len(data)
            time.sleep(1)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {station_id}: {e}")
            break
    return station_data

# Open the filtered CSV file with stations that have 2019 data
with open('us_weather_stations.csv', 'r') as infile, open('all_weather_data_2019.csv', 'w', newline='') as outfile:
    reader = csv.DictReader(infile)
    fieldnames = ['station_id', 'date', 'datatype', 'value', 'attributes']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    # Loop through each station in the filtered file
    for row in reader:
        station_id = row['Station ID']
        
        # Check if the station has any data in 2019 (avoid redundant API requests)
        if has_2019_data(station_id):
            print(f"Fetching data for station {station_id}...")
            station_data = get_station_data(station_id)
            
            # Write the station data to the CSV file
            for entry in station_data:
                writer.writerow({
                    'station_id': entry['station_id'],
                    'date': entry['date'],
                    'datatype': entry['datatype'],
                    'value': entry['value'],
                    'attributes': entry['attributes']
                })
        else:
            print(f"Station {station_id} has no data from 2019.")
            
print("Data collection complete. Saved to 'all_weather_data_2019.csv'.")
