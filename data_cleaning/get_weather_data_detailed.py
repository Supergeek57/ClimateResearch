import requests
import csv
from datetime import datetime

# Your NOAA API Token
API_TOKEN = 'lOOvrVZobgoKOHZTPLgdnvivcLvutwjg'
BASE_URL = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/'

# Define headers for authentication
HEADERS = {'token': API_TOKEN}

# Function to fetch daily weather data for a station
def fetch_weather_data(station_id
, start_date, end_date):
    all_weather_data = []
    offset = 0
    limit = 1000  # Max records per request

    # Data parameters for TMAX, TMIN, and PRCP
    data_params = {
        'datasetid': 'GHCND',           # Global Historical Climatology Network Daily dataset
        #'datatypeid': ['TMAX', 'TMIN', 'PRCP'],  # Data types to retrieve
        #'stationid': station_id,        # Unique station ID
        'startdate': start_date,        # Start of the date range
        'enddate': end_date,            # End of the date range
        #'limit': limit,                 # Limit the number of records per request
        #'offset': offset                # Start at offset 0
    }

    while True:
        # Make the request for weather data
        response = requests.get(BASE_URL + 'data', headers=HEADERS, params=data_params)
        if response.status_code == 200:
            weather_data = response.json().get('results', [])
            if not weather_data:
                # Break the loop if no more data is returned
                break
            all_weather_data.extend(weather_data)

            # Update the offset for the next request
            data_params['offset'] += limit
        else:
            print(f"Error fetching data for station {station_id}: {response.status_code}: {response.text}")
            print(str(response))
            break

    return all_weather_data

# Function to save the fetched data into a CSV file
def save_weather_data_to_csv(weather_data, output_file):
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(['Station ID', 'Date', 'Data Type', 'Value'])

        # Write each weather record to the CSV
        for data in weather_data:
            writer.writerow([
                data.get('station', ''),
                data.get('date', ''),
                data.get('datatype', ''),
                data.get('value', '')
            ])

# Main function to orchestrate data fetching and saving
def main():
    # Load your stations from CSV
    stations = []
    with open('us_weather_stations.csv', newline='') as station_file:
        reader = csv.DictReader(station_file)
        for row in reader:
            stations.append(row['Station ID'])

    # Define date range for the past 10 years
    start_date = '2019-01-01'
    end_date = '2019-12-31'

    # Loop through each station and fetch weather data
    for station_id in stations:
        print(f"Fetching data for station {station_id}...")
        weather_data = fetch_weather_data(station_id, start_date, end_date)
        
        if weather_data:
            # Save the data for each station to a CSV
            output_file = f"{station_id}_weather_data.csv"
            save_weather_data_to_csv(weather_data, output_file)
            print(f"Saved data for {station_id} to {output_file}")
        else:
            print(f"No data available for station {station_id}")

# Run the script
if __name__ == '__main__':
    main()
