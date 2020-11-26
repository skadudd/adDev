
import requests
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
import signaturehelper
import json

uri = '/ncc/keywords'
method = 'GET'
def get_header(method, uri, api_key, secret_key, customer_id):
    timestamp = str(round(time.time() * 1000))
    signature = signaturehelper.Signature.generate(timestamp, method, uri, SECRET_KEY)
    return {'Content-Type': 'application/json; charset=UTF-8', 'X-Timestamp': timestamp, 'X-API-KEY': API_KEY, 'X-Customer': str(CUSTOMER_ID), 'X-Signature': signature}

BASE_URL = 'https://api.naver.com'
API_KEY = '0100000000adc996fd9c6660f2496ec0f64a1ce8c5688874b0d0f5074d8f98b0fadd4793b9'
SECRET_KEY = 'AQAAAACtyZb9nGZg8kluwPZKHOjFpb6b54doFnHnBVokUWhNFw=='
CUSTOMER_ID = '1158940'

path = '/Users/maketing/adDev/kwd_combiner'
today = date.today()
db = []
# df = pd.read_csv('/Users/maketing/adDev/kwd_combiner/created_query/2020_11_CNC가공_필터된키워드.csv')
# df_cp = pd.read_csv('/Users/maketing/adDev/kwd_combiner/created_query/2020_11_부산시제품_필터된키워드.csv')

group_list = [
'grp-a001-01-000000017680513',
'grp-a001-01-000000017680514',
'grp-a001-01-000000017680515',
'grp-a001-01-000000017680516',
'grp-a001-01-000000017680517',
'grp-a001-01-000000017680518',
'grp-a001-01-000000017680519',
'grp-a001-01-000000017680520',
'grp-a001-01-000000017680521',
'grp-a001-01-000000017680522',
'grp-a001-01-000000017680523',
'grp-a001-01-000000017680524'
]

for v in group_list:
    r = requests.get(BASE_URL + uri, params={'nccAdgroupId': v}, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

    print("response status_code = {}".format(r.status_code))
    #print("response body = {}".format(r.json()))
    kwds = r.json()
    
    df = pd.DataFrame.from_dict(kwds)
    db.append(df)
    
result = pd.concat(db)
result .to_csv(Path(path, f'{today.year}_{today.month}_기존키워드.csv'), index=False)