import pandas as pd
import csv
import glob
import os
from pathlib import Path
input_file = 'merge'
allFile_list = glob.glob(os.path.join(input_file, '*.csv'))
all_data = []
for file in allFile_list:
    df = pd.read_csv(file)
    all_data.append(df)
data_combine = pd.concat(all_data, axis=0, ignore_index=True)
data_combine.to_csv(Path(input_file, 'combined.csv'), index=False )