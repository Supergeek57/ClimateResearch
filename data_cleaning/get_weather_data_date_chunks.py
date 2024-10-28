import requests
import csv
from datetime import datetime, timedelta

# Your NOAA API Token
API_TOKEN = 'lOOvrVZobgoKOHZTPLgdnvivcLvutwjg'
BASE_URL = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/'

# Define headers for authentication
HEADERS = {'token': API_TOKEN}

def fetch_weather_data(station_id, start_date, end_date):
    all_weather_data = []
    offset = 0
    limit = 1000  # Max records per request

    # Data parameters for TMAX, TMIN, and PRCP
    data_params = {
        'datasetid': 'GHCND',           # Global Historical Climatology Network Daily dataset
        #'datatypeid': ['TMAX', 'TMIN', 'PRCP'],  # Data types to retrieve
        'stationid': station_id,        # Unique station ID
        'startdate': start_date,        # Start of the date range
        'enddate': end_date,            # End of the date range
        'limit': limit,                 # Limit the number of records per request
        'offset': offset                # Start at offset 0
    }

    while True:
        # Make the request for weather data
        response = requests.get(BASE_URL + 'data', headers=HEADERS, params=data_params)

        if response.status_code == 200:
            weather_data = response.json().get('results', [])
            if not weather_data:
                break  # No more data, exit the loop
            all_weather_data.extend(weather_data)
            # Update the offset to get the next set of records
            offset += limit
            data_params['offset'] = offset
        else:
            print(f"Error fetching data for station {station_id} ({start_date} to {end_date}): {response.status_code}")
            print(response.text)  # Print the error message from the API
            break

    return all_weather_data

def daterange(start_date, end_date, delta):
    current_date = start_date
    while current_date < end_date:
        next_date = current_date + delta
        yield current_date, min(next_date, end_date)
        current_date = next_date

def main():
    # Load your stations from CSV
    stations = []
    with open('us_weather_stations.csv', newline='') as station_file:
        reader = csv.DictReader(station_file)
        for row in reader:
            stations.append(row['Station ID'])

    # Define the overall date range (past 10 years, for example)
    start_date = datetime(2014, 1, 1)
    end_date = datetime(2023, 12, 31)

    # Define the maximum date range allowed (less than a year, e.g., 6 months)
    delta = timedelta(days=365 // 2)  # 6 months

    # Loop through each station
    for station_id in stations:
        print(f"Fetching data for station: {station_id}")

        # Loop through date ranges in chunks (6 months)
        for start_chunk, end_chunk in daterange(start_date, end_date, delta):
            start_str = start_chunk.strftime('%Y-%m-%d')
            end_str = end_chunk.strftime('%Y-%m-%d')
            print(f"  Date range: {start_str} to {end_str}")

            weather_data = fetch_weather_data(station_id, start_str, end_str)
            print(f"  Retrieved {len(weather_data)} records for station {station_id} ({start_str} to {end_str})")

            # Optionally save data to CSV or handle the data as needed

if __name__ == '__main__':
    main()
