import os
import pandas as pd

def parse_dly_file(file_path):
    data = []
    
    with open(file_path, 'r') as file:
        for line in file:
            station_id = line[:11]
            year = line[11:15]
            month = line[15:17]
            element = line[17:21]
            
            for day in range(31):
                value = line[21 + day * 8:26 + day * 8].strip()
                mflag = line[26 + day * 8:27 + day * 8].strip()
                qflag = line[27 + day * 8:28 + day * 8].strip()
                sflag = line[28 + day * 8:29 + day * 8].strip()
                
                if value != "-9999":  # Missing value indicator
                    day_str = f"{int(day) + 1:02d}"  # Add 1 to get day of the month
                    date = f"{year}-{month}-{day_str}"
                    data.append([station_id, date, element, value, mflag, qflag, sflag])
    
    # Return the parsed data as a DataFrame
    df = pd.DataFrame(data, columns=['station_id', 'date', 'element', 'value', 'mflag', 'qflag', 'sflag'])
    return df

# Directory containing .dly files
dly_directory = '/Users/hollandamazonia/Downloads/ghcnd_all/ghcnd_all'
output_csv = 'merged_data.csv'

# Open the output CSV file for writing
with open(output_csv, 'w') as output_file:
    # Write the header
    output_file.write('station_id,date,element,value,mflag,qflag,sflag\n')
    
    # Loop through all .dly files and process them one by one
    for filename in os.listdir(dly_directory):
        if filename.endswith('.dly'):
            file_path = os.path.join(dly_directory, filename)
            print(f"Processing file: {file_path}")
            
            # Parse the .dly file into a DataFrame
            df = parse_dly_file(file_path)
            
            # Append the data to the CSV file in chunks to avoid memory issues
            df.to_csv(output_file, header=False, index=False)

print(f"Data successfully saved to {output_csv}")
