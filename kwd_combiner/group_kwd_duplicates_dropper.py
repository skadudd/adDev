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

path = '/Users/maketing/adDev/kwd_combiner/created_query'
today = date.today()
df = pd.read_csv('/Users/maketing/adDev/kwd_combiner/created_query/2020_11_CNC가공_필터된키워드.csv')
df_cp = pd.read_csv('/Users/maketing/adDev/kwd_combiner/created_query/2020_11_부산시제품_필터된키워드.csv')

kwd = df['연관 검색어'][0]

""" 합치고 중복 제거 코드
frames = []
frames.append(df)
frames.append(df_cp)
df2 = pd.concat(frames) 

df3 = df2.drop_duplicates(['연관 검색어'],keep='first')
print(len(df3))
"""

df3.to_csv(Path(path, f'{today.year}_{today.month}_{kwd}_그룹키워드.csv'), index=False)

