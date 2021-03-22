# -*- coding: utf-8 -*-
import re
import time
from datetime import date
import numpy
import math
import time
from pathlib import Path
import pandas as pd
from pandas import DataFrame
import random
from itertools import product

path = '/Users/kim/Desktop'
today = date.today()
df = pd.read_csv('/Users/kim/Desktop/crowdy.csv',index_col=0)
df_cp = pd.read_csv('/Users/kim/Desktop/crowdy_closed.csv',index_col=0)

frames = []
frames.append(df)
frames.append(df_cp)
df2 = pd.concat(frames) 

df3 = df2.drop_duplicates(['email'],keep='first')
print(len(df3))


df3.to_csv(Path(path, f'{today.year}_{today.month}_crowdy.csv'), index=False)