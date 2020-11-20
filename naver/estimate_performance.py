import time
import random
import requests
import json
from pathlib import Path
from datetime import date
import numpy as np
import re
import pandas as pd
from pandas import DataFrame
from functools import reduce
import signaturehelper

today = date.today()
monthly_performance_path = '/Users/maketing/adDev/NSA_rel_keyword/monthly_performance_raw_data'
query_path = '/Users/maketing/adDev/NSA_rel_keyword/filtered_query.csv'

BASE_URL = 'https://api.naver.com'
API_KEY = '0100000000adc996fd9c6660f2496ec0f64a1ce8c5688874b0d0f5074d8f98b0fadd4793b9'
SECRET_KEY = 'AQAAAACtyZb9nGZg8kluwPZKHOjFpb6b54doFnHnBVokUWhNFw=='
CUSTOMER_ID = '1158940'

def get_header(method, uri, api_key, secret_key, customer_id):
    timestamp = str(round(time.time() * 1000))
    signature = signaturehelper.Signature.generate(timestamp, method, uri, SECRET_KEY)
    return {'Content-Type': 'application/json; charset=UTF-8', 'X-Timestamp': timestamp, 'X-API-KEY': API_KEY, 'X-Customer': str(CUSTOMER_ID), 'X-Signature': signature}



def get_query():
    df = pd.read_csv(monthly_performance_path + '/202011_CNC_test.csv',header=None)
    return df

def get_rows(query):
    list_of_rows = []
    list_of_kwds = []
    
    for num in range(len(query)):
        inner = []

        if num == 0:
            continue
        row = query.iloc[num]
        list_of_kwds.append(row[0])
        row.pop(0)
        for value in row:
            inner.append(value)
        list_of_rows.append(inner)

    return list_of_kwds,list_of_rows

def handle_data(json_data):
    kwd = json_data['keyword']
    rank = pd.Series([1,2,3,4,5,6,7,8,9,10])
    
    df = pd.DataFrame.from_dict(json_data['estimate'])
    df.insert(0,'rank',rank,allow_duplicates = False)
    df.insert(0,'keyword',kwd,allow_duplicates = False)
    df['cpc'] = round(df['cost']/df['clicks'],0)
    df = df[['keyword','rank','bid','impressions','clicks','cpc','cost']]

    return df

def get_data(kwd_list, row_list):
    # bids[] : The maximum of 100 bids can be requested at once.
    uri = '/estimate/performance/keyword'
    method = 'POST'
    handled_df = []
    
    for v in range(len(kwd_list)):
        r = requests.post(BASE_URL + uri, json={'device': 'PC', 'keywordplus': True, 'key': kwd_list[v], 'bids':row_list[v] }, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

        print("response status_code = {}".format(r.status_code))
        json_data = json.loads(r.text)
        df = handle_data(json_data)
        handled_df.append(df)

    return handled_df

def concat_df(data):
    frames = []
    for i in range(len(data)):
        frames.append(data[i])
    result = pd.concat(frames)

    return result

def init() :
    DB = []
    query = get_query()
    main_kwd = query[0][1]
    kwd_list,row_list = get_rows(query)
    list_of_df = get_data(kwd_list,row_list)
    concated_df = concat_df(list_of_df)

    print(concated_df)
    #print(kwd_list)
    #print(row_values)

init()