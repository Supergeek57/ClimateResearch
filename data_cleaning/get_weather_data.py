import requests
import csv

# Your NOAA API Token
API_TOKEN = 'lOOvrVZobgoKOHZTPLgdnvivcLvutwjg'
BASE_URL = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/'

# Define headers for authentication
HEADERS = {'token': API_TOKEN}

# Define the base parameters to get U.S. weather stations
station_params = {
    'locationid': 'FIPS:US',  # Location for US (FIPS code)
    'datasetid': 'GHCND',     # Global Historical Climatology Network Daily
    'limit': 1000,            # Max number of stations per request (1000 is the max)
    'offset': 0               # Offset for pagination
}

# Function to fetch station data with pagination
def fetch_all_stations():
    all_stations = []
    while True:
        # Make the request for the current batch of stations
        response = requests.get(BASE_URL + 'stations', headers=HEADERS, params=station_params)
        if response.status_code == 200:
            stations = response.json().get('results', [])
            if not stations:
                # Stop if no more stations are returned
                break
            all_stations.extend(stations)
            print(f"Fetched {len(stations)} stations, total: {len(all_stations)}")

            # Update the offset for the next batch
            station_params['offset'] += station_params['limit']
        else:
            print(f"Error fetching stations: {response.status_code}")
            break
    return all_stations

# Save the fetched data into a CSV file
def save_stations_to_csv(stations):
    with open('us_weather_stations.csv', mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write the header row
        writer.writerow(['Station ID', 'Station Name', 'Latitude', 'Longitude', 'Elevation', 'Min Date', 'Max Date'])
        
        # Write the station data rows
        for station in stations:
            writer.writerow([
                station.get('id', ''),
                station.get('name', ''),
                station.get('latitude', ''),
                station.get('longitude', ''),
                station.get('elevation', ''),
                station.get('mindate', ''),
                station.get('maxdate', '')
            ])

# Main function to orchestrate data fetching and saving
def main():
    print("Fetching all station data...")
    stations = fetch_all_stations()
    
    print(f"Fetched {len(stations)} stations. Saving to CSV...")
    save_stations_to_csv(stations)
    
    print("Data saved to us_weather_stations.csv")

# Run the script
if __name__ == '__main__':
    main()
