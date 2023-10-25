import os
import pprint

import pandas as pd

ALL_ATTACKS_CSV_FILE = '/Users/p0tt3r/coursework/ISP/repy_v2/scripts/TARGET_FOLDER/All_Attacks_matrix.csv'


def merge_csvs(csv_files):
    # Initialize a list to store dataframes
    dfs = []

    # Read each CSV into a dataframe and append to the list
    for path in csv_files:
        dfs.append(pd.read_csv(path))

    # Use the reduce function from the functools module to sequentially merge dataframes
    from functools import reduce
    merged_df = reduce(lambda left, right: pd.merge(
        left, right, on='All attack files-->'), dfs)

    # Save the merged dataframe to a new CSV
    merged_df.to_csv(ALL_ATTACKS_CSV_FILE, index=False)


attackcases = os.path.join(os.getcwd(), 'attackcases_')

csv_files = [os.path.join(attackcases + str(f),
                          'All_Attacks_matrix.csv') for f in range(1, 9)]

pprint.pprint(csv_files)

merge_csvs(csv_files)
