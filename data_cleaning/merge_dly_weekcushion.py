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
            
            # Skip files not in 2018, 2019, or 2020
            if year not in ["2018", "2019", "2020"]:
                continue
            
            for day in range(31):
                day_num = day + 1
                value = line[21 + day * 8:26 + day * 8].strip()
                mflag = line[26 + day * 8:27 + day * 8].strip()
                qflag = line[27 + day * 8:28 + day * 8].strip()
                sflag = line[28 + day * 8:29 + day * 8].strip()
                
                # Construct date and apply filtering criteria
                day_str = f"{day_num:02d}"
                date = f"{year}-{month}-{day_str}"
                
                # Check if the date is within the desired range
                if (
                    (year == "2019") or
                    (year == "2018" and month == "12" and day_num >= 1) or
                    (year == "2020" and month == "01" and day_num <= 31)
                ):
                    if value != "-9999":  # Skip missing values
                        data.append([station_id, date, element, value, mflag, qflag, sflag])
    
    # Convert data to DataFrame
    df = pd.DataFrame(data, columns=['station_id', 'date', 'element', 'value', 'mflag', 'qflag', 'sflag'])
    return df

# Specify the directory containing .dly files
dly_directory = '/Users/hollandamazonia/Downloads/ghcnd_all/ghcnd_all'
output_csv = '2019_data_week_cushion.csv'

# Remove the file if it exists to avoid appending to old data
if os.path.exists(output_csv):
    os.remove(output_csv)

# Process files in batches
batch_size = 100  # Adjust based on memory and disk space
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

print("Filtered data with 2019 and edge weeks saved successfully.")
