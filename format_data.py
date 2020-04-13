import numpy as np
import pandas as pd

raw_data = np.genfromtxt('Trains.csv', delimiter=',', skip_header=0, dtype=str)

for row in raw_data[1:, :]:
    for i in range(1,5):
        split_time = row[i].split(".")
        if len(split_time) == 1:
            row[i] += ".00"
        elif len(split_time) == 2 and len(split_time[1]) == 1:
            row[i] += "0"

        row[i] = row[i].replace(".", ":")

raw_df = pd.DataFrame(data=raw_data[1:, :], columns=raw_data[0, :])

gwr_df = raw_df.loc[raw_df['Company'] == 'GWR']
thameslink_df = raw_df.loc[raw_df['Company'] == 'Thameslink']

gwr_data = gwr_df.values
thameslink_data = thameslink_df.values

np.savez("gwr_thameslink.npz", gwr_data, thameslink_data)
