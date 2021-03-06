import time
import random
import requests
import json
import signaturehelper

import pandas as pd
from pandas import DataFrame
from datetime import date
from pathlib import Path
import csv


BASE_URL = 'https://api.naver.com'
API_KEY = '0100000000adc996fd9c6660f2496ec0f64a1ce8c5688874b0d0f5074d8f98b0fadd4793b9'
SECRET_KEY = 'AQAAAACtyZb9nGZg8kluwPZKHOjFpb6b54doFnHnBVokUWhNFw=='
CUSTOMER_ID = '1158940'

today = date.today()
montly_data = '../NSA_rel_keyword/monthly_raw_data'
request_query_path = '../NSA_rel_keyword/'

def get_header(method, uri, api_key, secret_key, customer_id):
    timestamp = str(round(time.time() * 1000))
    signature = signaturehelper.Signature.generate(timestamp, method, uri, SECRET_KEY)
    return {'Content-Type': 'application/json; charset=UTF-8', 'X-Timestamp': timestamp, 'X-API-KEY': API_KEY, 'X-Customer': str(CUSTOMER_ID), 'X-Signature': signature}

def get_query():
    df = pd.read_csv('../NSA_rel_keyword/query.csv',header=None)
    return df
    # len_of_query = len(df.index)
    # print(df[0][1])  

# def concat_df(data):
#     frames = []
#     for i in range(len(data)):
#         frames.append(data[i])
#     result = pd.concat(frames,join="inner")

#     return result

def get_data(kwd):
    uri = '/keywordstool'
    method = 'GET'
    params = {'hintKeywords': kwd, 'showDetail' : 1}
    print(1,kwd)
    r = requests.get(BASE_URL + uri, params=params, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))
    print("response status_code = {}".format(r.status_code))
    # print("response body = {}".format(r.json()))
    json_data = json.loads(r.text)

    df = pd.DataFrame.from_dict(json_data['keywordList'])
    df.columns = ['연관 검색어','PC 월간 검색수','모바일 월간 검색수','PC 월평균 클릭수','모바일 월평균 클릭수','PC 월평균 클릭률','모바일 월평균 클릭율','월평균 노출 광고수','경쟁 정도']
    df = df[['연관 검색어','PC 월간 검색수','PC 월평균 클릭수','PC 월평균 클릭률','모바일 월간 검색수','모바일 월평균 클릭수','모바일 월평균 클릭율','월평균 노출 광고수','경쟁 정도']]
    
    return df
    
def write_csv(df,kwd):
    df.to_csv(Path(montly_data, f'{today}_{kwd}_네이버검색광고_키워드.csv'), index=False)

def concat_csv(db):
    frames = []
    for i in range(len(db)):
        frames.append(db[i])
    result = pd.concat(frames)
    result = result.drop_duplicates(['연관 검색어'],keep='first')
    write_csv(result,'merged')

    return

def init():
    db = []
    query = get_query()
    len_of_query = len(query.index) - 1

    for i in range(len_of_query):
        i += 1
        kwd = query[0][i]
        print(kwd)
        time.sleep(5)
        df = get_data(kwd)
        #concated_df = concat_df(df)
        db.append(df)
        write_csv(df,kwd)
    concat_csv(db)
init()