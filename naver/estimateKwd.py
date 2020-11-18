import time
import random
import requests
import json
from datetime import date

import signaturehelper

import pandas as pd
from pandas import DataFrame

today = date.today()
montly_kwd_performance = '/Users/maketing/adDev/NSA_rel_keyword/montly_performance_raw_data'
request_query_path = '/Users/maketing/adDev/NSA_rel_keyword/'


def get_header(method, uri, api_key, secret_key, customer_id):
    timestamp = str(round(time.time() * 1000))
    signature = signaturehelper.Signature.generate(timestamp, method, uri, SECRET_KEY)
    return {'Content-Type': 'application/json; charset=UTF-8', 'X-Timestamp': timestamp, 'X-API-KEY': API_KEY, 'X-Customer': str(CUSTOMER_ID), 'X-Signature': signature}


BASE_URL = 'https://api.naver.com'
API_KEY = '0100000000adc996fd9c6660f2496ec0f64a1ce8c5688874b0d0f5074d8f98b0fadd4793b9'
SECRET_KEY = 'AQAAAACtyZb9nGZg8kluwPZKHOjFpb6b54doFnHnBVokUWhNFw=='
CUSTOMER_ID = '1158940'


# # Estimate Usage Sample

# # 1. average-position-bid
# ## items : The maximum of 200 keys can be requested at once.
# uri = '/estimate/average-position-bid/keyword'
# method = 'POST'
# r = requests.post(BASE_URL + uri, json={'device': 'PC', 'items': [{'key': '금속가공', 'position': 7}, {'key': '중고차', 'position': 7}, {'key': '자전거여행', 'position': 9}]}, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

# print("#response status_code = {}".format(r.status_code))
# print("#response body = {}".format(r.json()))

# # 5. performance-bulk
# #items : The maximum of 200 items can be requested at once.

# uri = '/estimate/performance-bulk'
# method = 'POST'
# r = requests.post(BASE_URL + uri, json={'items': [{'device': 'PC', 'keywordplus': True, 'keyword': '제주여행', 'bid': 70}, {'device': 'PC', 'keywordplus': True, 'keyword': '제주도', 'bid': 80}, {'device': 'PC', 'keywordplus': True, 'keyword': '제주도맛집', 'bid': 90}, ]}, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

# print("response status_code = {}".format(r.status_code))
# print("response body = {}".format(r.json()))

# # # 2. exposure-minimum-bid
# ## items : The maximum of 200 keys can be requested at once.

# uri = '/estimate/exposure-minimum-bid/keyword'
# method = 'POST'
# r = requests.post(BASE_URL + uri, json={'device': 'PC', 'period': 'MONTH', 'items': ['제주여행', '중고차', '자전거여행']}, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))
# # 
# print("response status_code = {}".format(r.status_code))
# print("response body = {}".format(r.json()))

# # 3. median-bid
# ## items : The maximum of 200 keys can be requested at once.
# uri = '/estimate/median-bid/keyword'
# method = 'POST'
# r = requests.post(BASE_URL + uri, json={'device': 'PC', 'period': 'MONTH', 'items': ['금속가공', '중고차', '자전거여행']}, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

# print("response status_code = {}".format(r.status_code))
# print("response body = {}".format(r.json()))


# # 4. performance
## bids[] : The maximum of 100 bids can be requested at once.
# uri = '/estimate/performance/keyword'
# method = 'POST'
# r = requests.post(BASE_URL + uri, json={'device': 'PC', 'keywordplus': True, 'key': '중고차', 'bids': [100, 500, 1000, 1500, 2000, 3000, 5000]}, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

# print("response status_code = {}".format(r.status_code))
# print("response body = {}".format(r.json()))

def get_query():
    df = pd.read_csv('/Users/maketing/adDev/NSA_rel_keyword/filtered_query.csv',header=None)
    return df


def sample_data_set(query):
    len_of_query = len(query.index) - 1
    list_of_data_set = []
    data_set = []

    for i in range(len_of_query):
        i += 1
        kwd = query[0][i]
        kwd_set = dict(key = kwd, position = 1)
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
        'device': 'PC', 
        'items': kwd
        }, 
        headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

    print("#response status_code = {}".format(r.status_code))
    #print("#response body = {}".format(r.json()))
    json_data = json.loads(r.text)
    df = pd.DataFrame.from_dict(json_data['estimate'])

    return df

def request_estimate(data):
    df_list = []
    len_of_list_of_data_set = len(data)

    for i in range(len_of_list_of_data_set):
        df = get_data(data[i])
        df_list.append(df)
    
    return df_list


def merge_df(data):
    #데이터프레임 혼합. 2가지 case.
    #200개 초과한 동일한 순위 데이터 종적 혼합.
    #순위 데이터프레임 마다 각자 혼합된 데이터셋 존재.
    #각 데이터프레임 횡적 혼합.
    print(len(data))
    a = data[0]
    b = data[1]
    print(pd.merge(a,b,on='keyword'))
    #print(a)
    #print(a.merge(b))
    


# def write_csv():
#     df = pd.DataFrame.from_dict(json_data['keywordList'])
#     df.to_csv(Path(montly_data, f'{today}_{kwd}_네이버검색광고_키워드.csv'), index=False)

def init() :
    query = get_query()
    data = sample_data_set(query)
    list_of_dataframe = request_estimate(data)
    merge_df(list_of_dataframe)
    
    #write_csv()
    #merge_csv()
    #clear_dir()


init()





