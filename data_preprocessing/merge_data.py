import pandas as pd
import glob
import os
from utils.helpers import save_to_csv

def merge_csv_files(directory, output_filename="merged_file.csv"):
    """Merges all CSV files in a directory into a single CSV file.

    Args:
        directory (str): The path to the directory containing the CSV files.
        output_filename (str, optional): The name of the output CSV file. 
                                         Defaults to "merged_file.csv".
    """
    all_filenames = glob.glob(os.path.join(directory, "*.csv"))
    all_df = []
    for f in all_filenames:
        df = pd.read_csv(f)
        all_df.append(df)
    merged_df = pd.concat(all_df, ignore_index=True)
    folder = 'data/merged/'
    save_to_csv(merged_df, output_filename, folder)
    #merged_df.to_csv(output_filename, index=False)
    print(f"Successfully merged {len(all_filenames)} CSV files into '{output_filename}'")

# You can also specify a custom output filename:
# merge_csv_files(directory_path, "combined_data.csv")