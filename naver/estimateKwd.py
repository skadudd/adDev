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

monthly_performance_path = '../NSA_rel_keyword/monthly_performance_raw_data'
query_path = '../NSA_rel_keyword/monthly_raw_data/금형키워드.csv'
device = 'PC'


def get_header(method, uri, api_key, secret_key, customer_id):
    timestamp = str(round(time.time() * 1000))
    signature = signaturehelper.Signature.generate(timestamp, method, uri, SECRET_KEY)
    return {'Content-Type': 'application/json; charset=UTF-8', 'X-Timestamp': timestamp, 'X-API-KEY': API_KEY, 'X-Customer': str(CUSTOMER_ID), 'X-Signature': signature}


BASE_URL = 'https://api.naver.com'
API_KEY = '0100000000adc996fd9c6660f2496ec0f64a1ce8c5688874b0d0f5074d8f98b0fadd4793b9'
SECRET_KEY = 'AQAAAACtyZb9nGZg8kluwPZKHOjFpb6b54doFnHnBVokUWhNFw=='
CUSTOMER_ID = '1158940'

def get_query():
    df = pd.read_csv(query_path,header=None)
    return df


def sample_data_set(query,num):
    len_of_query = len(query.index) - 1
    list_of_data_set = []
    data_set = []

    for i in range(len_of_query):
        i += 1
        kwd = query[0][i]
        kwd_set = dict(key = kwd, position = num)
        data_set.append(kwd_set)
        #print(len(data_set))
        if len(data_set) == 200 :
            list_of_data_set.append(data_set)
            data_set = []
        if i == len_of_query :
            list_of_data_set.append(data_set)
    
    return list_of_data_set    

def get_data(kwd):
    # 1. average-position-bid
    ## items : The maximum of 200 keys can be requested at once.
    uri = '/estimate/average-position-bid/keyword'
    method = 'POST'
    r = requests.post(BASE_URL + uri, json={
        'device': device, 
        'items': kwd
        }, 
        headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

    print("#response status_code = {}".format(r.status_code))
    #print("#response body = {}".format(r.json()))
    json_data = json.loads(r.text)
    df = pd.DataFrame.from_dict(json_data['estimate'])

    return df

def request_estimate(data,i):
    bid_and_position = 'bidding' + str(i) + 'st '
    df_list = []
    len_of_list_of_data_set = len(data)

    for i in range(len_of_list_of_data_set):
        df = get_data(data[i])
        sorted_df = handle_column(df,bid_and_position)
        df_list.append(sorted_df)
    
    return df_list

def handle_column(df,bid_and_position) :
    df.columns = [bid_and_position,'keyword','position']
    del df['position']
    df = df[['keyword',bid_and_position]]

    return df

def concat_df(data):
    frames = []
    for i in range(len(data)):
        frames.append(data[i])
    result = pd.concat(frames)

    return result

def merge_df(data):
    df_merged = reduce(lambda left,right: pd.merge(left,right,on=['keyword']), data)
    df_merged = df_merged.drop_duplicates(['keyword'],keep='first')
    return df_merged

def write_csv(data,kwd):
    print('write_csv')
    data.to_csv(Path(monthly_performance_path, f'{today.year}{today.month}_{kwd}_구좌순위별_비딩가.csv'), index=False)

def init() :
    DB = []
    query = get_query()
    main_kwd = query[0][1]
    if device is 'PC':
        range_itterate = 10
    else :
        range_itterate = 5
    print(range_itterate)
    for i in range(range_itterate):
        i += 1
        data = sample_data_set(query,i)
        list_of_dataframe = request_estimate(data,i)
        distributed_df = concat_df(list_of_dataframe)
        DB.append(distributed_df)
        time.sleep(2)
    
    df_of_bid = merge_df(DB)
    print(df_of_bid)
    write_csv(df_of_bid,main_kwd)

init()