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

#키워드 json화
df = pd.read_csv('/Users/maketing/adDev/naver/test.csv',header=None)
kwd = df[0][1]
kwd_set = dict(keyword = kwd, useGroupBidAmt = False, bidAmt = 70)
print(kwd_set)

#키워드업로드 리퀘스트
# 1. CREATE AdKeyword

def get_header(method, uri, api_key, secret_key, customer_id):
    timestamp = str(round(time.time() * 1000))
    signature = signaturehelper.Signature.generate(timestamp, method, uri, SECRET_KEY)
    return {'Content-Type': 'application/json; charset=UTF-8', 'X-Timestamp': timestamp, 'X-API-KEY': API_KEY, 'X-Customer': str(CUSTOMER_ID), 'X-Signature': signature}


BASE_URL = 'https://api.naver.com'
API_KEY = '0100000000adc996fd9c6660f2496ec0f64a1ce8c5688874b0d0f5074d8f98b0fadd4793b9'
SECRET_KEY = 'AQAAAACtyZb9nGZg8kluwPZKHOjFpb6b54doFnHnBVokUWhNFw=='
CUSTOMER_ID = '1158940'


uri = '/ncc/keywords'
method = 'POST'
r = requests.post(BASE_URL + uri, params={
    'nccAdgroupId': 'grp-a001-01-000000018431679'}, 
    json=[kwd_set], 
    headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

print("response status_code = {}".format(r.status_code))
print("response body = {}".format(r.json()))

created_adkeyword = r.json()[0]