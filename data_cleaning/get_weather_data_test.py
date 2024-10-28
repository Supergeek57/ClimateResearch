import requests
import csv
from datetime import datetime

# Your NOAA API Token
API_TOKEN = 'lOOvrVZobgoKOHZTPLgdnvivcLvutwjg'
BASE_URL = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/'

# Define headers for authentication
HEADERS = {'token': API_TOKEN}

def fetch_weather_data(start_date, end_date):
    all_weather_data = []
    offset = 0
    limit = 1000  # Max records per request

    # Data parameters for TMAX, TMIN, and PRCP
    data_params = {
        'datasetid': 'GHCND',           # Global Historical Climatology Network Daily dataset
        'startdate': start_date,        # Start of the date range
        'enddate': end_date,            # End of the date range
    }

    response = requests.get(BASE_URL + 'data', headers=HEADERS, params=data_params)
    if response.status_code == 200:
        weather_data = response.json().get('results', [])
        all_weather_data.extend(weather_data)
    else:
        print(f"Error fetching data: {response.status_code}")
        print(str(response.content))

    return all_weather_data

def main():
    # Load your stations from CSV
    stations = []
    with open('us_weather_stations.csv', newline='') as station_file:
        reader = csv.DictReader(station_file)
        for row in reader:
            stations.append(row['Station ID'])

    # Define date range for the past 10 years
    start_date = '2010-01-02'
    end_date = '2015-01-10'

    # Loop through each station and fetch weather data
    weather_data = fetch_weather_data(start_date, end_date)
    #print(weather_data)

if __name__ == '__main__':
    main()

