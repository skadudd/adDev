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

def get_header(method, uri, api_key, secret_key, customer_id):
    timestamp = str(round(time.time() * 1000))
    signature = signaturehelper.Signature.generate(timestamp, method, uri, SECRET_KEY)
    return {'Content-Type': 'application/json; charset=UTF-8', 'X-Timestamp': timestamp, 'X-API-KEY': API_KEY, 'X-Customer': str(CUSTOMER_ID), 'X-Signature': signature}

BASE_URL = 'https://api.naver.com'
API_KEY = '0100000000adc996fd9c6660f2496ec0f64a1ce8c5688874b0d0f5074d8f98b0fadd4793b9'
SECRET_KEY = 'AQAAAACtyZb9nGZg8kluwPZKHOjFpb6b54doFnHnBVokUWhNFw=='
CUSTOMER_ID = '1158940'

# a = {'keyword': '기계가공', 'useGroupBidAmt': False, 'bidAmt': 2300, 'links': {'pc': {'final': 'https://beta.creatable.com'}, 'mobile': {'final': 'https://beta.creatable.com'}}}
# print(json.dumps(a))
# for v in a:
    
#     n = 3
#     a[v] = [a[v][i * n:(i + 1) * n] for i in range((len(a[v]) + n - 1) // n )] 

# for v in a:
#     for s in a[v]:
#         print(v)
#         print(s)

# b = 'aaa'
# a[b].append(5)
# print(a[b])


def create_kwd_set(concated_df):
    ad_group = {
        '고관련인기' : 'grp-a001-01-000000018602440', 
        '고관련비인기' : 'grp-a001-01-000000018602500', 
        '저관련인기' : 'grp-a001-01-000000018602509', 
        '저관련비인기' : 'grp-a001-01-000000018602514'}
    atrred_kwd = {'고관련인기' : [], '고관련비인기' : [], '저관련인기' : [], '저관련비인기' : []}
    # index_title = ['고관련인기','고관련비인기','저관련인기','저관련비인기']

    for v in range(len(concated_df)):
        attr = concated_df.iloc[v]['attr'] 
        kwd = concated_df.iloc[v]['keyword']
        bid = concated_df.iloc[v]['bid']
        kwd_set = kwd_set_to_json(kwd,bid)
        print(kwd_set)
        atrred_kwd[attr].append(kwd_set)

    #list 나누기    
    for v in atrred_kwd :        
        n = 2
        atrred_kwd[v] = [atrred_kwd[v][i * n:(i + 1) * n] for i in range((len(atrred_kwd[v]) + n - 1) // n )] 
    #print(atrred_kwd)
    #네이버 요청
    for f in atrred_kwd:
        for s in atrred_kwd[f]:
            ad_group_name = ad_group[f]
            kwd_set = s
            request_upload_to_naver(kwd_set,ad_group_name)
    # kwd = concated_df['bid']['고관련비인기']
    # print(concated_df)
    # print(len(kwd))
    # print(kwd)

def kwd_set_to_json(kwd,bid):
    kapa_link = {
      "pc": {"final": "https://beta.creatable.com"},
      "mobile": {"final": "https://beta.creatable.com"}
    }
    
    kwd_set = dict(keyword = kwd, useGroupBidAmt = False, bidAmt = f'{bid}', links= kapa_link)
    json_kwd_set = json.dumps(kwd_set)

    return kwd_set

# 키워드업로드 리퀘스트
# 1. CREATE AdKeyword
def request_upload_to_naver(kwd_set,ad_group):
    print(kwd_set)
    print(ad_group)
    
    uri = '/ncc/keywords'
    method = 'POST'
    r = requests.post(BASE_URL + uri, params={
        'nccAdgroupId': ad_group}, 
        json = kwd_set, 
        headers= get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

    print("response status_code = {}".format(r.status_code))
    print("response body = {}".format(r.json()))
    print(len(kwd_set))

    
# def request_upload_to_naver2():

#     uri = '/ncc/keywords'
#     method = 'POST'
#     r = requests.post(BASE_URL + uri, params={
#         'nccAdgroupId': 'grp-a001-01-000000018602440'}, 
#         json= [{'keyword': 'CNC가공', 'useGroupBidAmt': False, 'bidAmt': 5370, 'links': {'pc': {'final': 'https://beta.creatable.com'}, 'mobile': {'final': 'https://beta.creatable.com'}}}],
#         headers= get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

#     print("response status_code = {}".format(r.status_code))
#     print("response body = {}".format(r.json()))
#     created_adkeyword = r.json()[0]

# request_upload_to_naver2()
# print(1)
