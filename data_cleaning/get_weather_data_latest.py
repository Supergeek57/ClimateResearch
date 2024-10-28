import requests
import csv
import time

# Your NOAA API token
api_token = 'lOOvrVZobgoKOHZTPLgdnvivcLvutwjg'
headers = {'token': api_token}

# Base URL for NOAA CDO API
base_url = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/data'

# Define the data you want to fetch (daily precipitation, max/min temperature)
data_params = {
    'datasetid': 'GHCND',
    'stationid': '',
    'startdate': '2019-01-01',
    'enddate': '2019-12-31',
    'limit': 1000,
    'offset': 0
}

# Function to get weather data for a station
def get_station_data(station_id):
    offset = 0
    station_data = []
    while True:
        #params = {**data_params, 'stationid': f'GHCND:{station_id}', 'offset': offset}
        print("Making API request...")
        data_params['stationid'] = station_id
        response = requests.get(base_url, headers=headers, params=data_params)
        if response.status_code != 200:
            print(f"Error fetching data for station {station_id}: {response.status_code}: {response.text}")
            print("Trying again...")
            continue
        else:
            print(f"Fetched data for station {station_id}, offset: {offset}")
        data = response.json().get('results', [])
        #data_txt = response.text
        #print(data_txt)
        if not data:
            break
        # Add station_id to each data entry
        for entry in data:
            entry['station_id'] = station_id
        station_data.extend(data)
        # offset += len(data)
        data_params['offset'] += len(data)
        
        # Avoid hitting the API rate limit
        time.sleep(1)  # Pause for 1 second between each request
    
    return station_data

# Open a single CSV file to write all data
with open('all_station_data_2019_NEW.csv', 'w', newline='') as outfile:
    writer = None  # This will be initialized after we fetch the first batch of data

    # Read station IDs from your CSV file
    with open('stations_with_data_2019.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # print(row)
            station_id = row['Station ID']
            data = get_station_data(station_id)
            print("Number of records: ", len(data))
            if data:  # Only write data if there's something to save
                # Initialize the CSV writer with the fieldnames if it's the first write
                if writer is None:
                    # Use fieldnames from the first record's keys (plus 'station_id')
                    writer = csv.DictWriter(outfile, fieldnames=data[0].keys())
                    writer.writeheader()

                # Write all the data for this station
                writer.writerows(data)
                print("Data written")

            # Optional: Additional sleep after processing each station
            time.sleep(1)  # Pause for 1 second after each station