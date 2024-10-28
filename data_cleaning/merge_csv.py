import pandas as pd
import glob
import os

# Specify the path where your CSV files are located
path = '/Users/hollandamazonia/Downloads/normals-hourly/*.csv'

# Use glob to get all CSV files matching the pattern
csv_files = glob.glob(path)

# Check if any files were found
if not csv_files:
    print("No CSV files found. Check your file path.")
else:
    print(f"Found {len(csv_files)} CSV files.")

# List to hold all dataframes
df_list = []

# Loop through all CSV files and read them into dataframes
for file in csv_files:
    print(f"Reading file: {file}")
    if os.path.getsize(file) > 0:  # Check if the file is not empty
        try:
            df = pd.read_csv(file)
            df_list.append(df)
            print(f"File {file} successfully loaded with {df.shape[0]} rows and {df.shape[1]} columns.")
        except pd.errors.EmptyDataError:
            print(f"File {file} is empty or cannot be read as a CSV.")
        except pd.errors.ParserError:
            print(f"File {file} has a parsing issue and could not be read.")
    else:
        print(f"File {file} is empty.")

# Check if any dataframes were loaded
if df_list:
    # Concatenate all dataframes
    merged_df = pd.concat(df_list, ignore_index=True)
    print(f"Successfully concatenated {len(df_list)} files into one dataframe with {merged_df.shape[0]} rows and {merged_df.shape[1]} columns.")
    
    # Save the merged dataframe to a new CSV file
    merged_df.to_csv('/Users/hollandamazonia/Downloads/weather_2025.csv', index=False)
    print("Merged file saved as 'weather_2025.csv'.")
else:
    print("No valid CSV files were loaded.")