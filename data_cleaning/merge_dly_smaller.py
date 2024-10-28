import os
import pandas as pd

def parse_dly_file(file_path):
    data = []
    
    with open(file_path, 'r') as file:
        for line in file:
            station_id = line[:11]
            year = line[11:15]
            
            # Filter only for records from the year 2019
            if year != "2019":
                continue
            
            month = line[15:17]
            element = line[17:21]
            
            for day in range(31):
                value = line[21 + day * 8:26 + day * 8].strip()
                mflag = line[26 + day * 8:27 + day * 8].strip()
                qflag = line[27 + day * 8:28 + day * 8].strip()
                sflag = line[28 + day * 8:29 + day * 8].strip()
                
                if value != "-9999":  # Skip missing values
                    day_str = f"{int(day) + 1:02d}"  # Add 1 to get day of the month
                    date = f"{year}-{month}-{day_str}"
                    data.append([station_id, date, element, value, mflag, qflag, sflag])
    
    # Convert data to DataFrame
    df = pd.DataFrame(data, columns=['station_id', 'date', 'element', 'value', 'mflag', 'qflag', 'sflag'])
    return df

# Specify the directory containing .dly files
dly_directory = '/Users/hollandamazonia/Downloads/ghcnd_all/ghcnd_all'
output_csv = 'filtered_2019_data_take2.csv'

# Remove the file if it exists to avoid appending to old data
if os.path.exists(output_csv):
    os.remove(output_csv)

# Process files in batches
batch_size = 100  # Adjust batch size based on available memory and disk space
all_files = [f for f in os.listdir(dly_directory) if f.endswith('.dly')]

# Loop through files in batches
for i in range(0, len(all_files), batch_size):
    batch_files = all_files[i:i + batch_size]
    batch_dfs = []
    
    for filename in batch_files:
        file_path = os.path.join(dly_directory, filename)
        df = parse_dly_file(file_path)
        batch_dfs.append(df)
    
    # Concatenate the batch of dataframes
    batch_df = pd.concat(batch_dfs, ignore_index=True)
    
    # Append the batch to the output CSV
    batch_df.to_csv(output_csv, mode='a', header=not os.path.exists(output_csv), index=False)
    print(f"Processed batch {i // batch_size + 1} of {len(all_files) // batch_size + 1}")

print("Filtered 2019 data successfully saved.")
