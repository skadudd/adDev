import time
import random
import requests
import json
import signaturehelper

import pandas as pd
from pandas import DataFrame

def get_header(method, uri, api_key, secret_key, customer_id):
    timestamp = str(round(time.time() * 1000))
    signature = signaturehelper.Signature.generate(timestamp, method, uri, SECRET_KEY)
    return {'Content-Type': 'application/json; charset=UTF-8', 'X-Timestamp': timestamp, 'X-API-KEY': API_KEY, 'X-Customer': str(CUSTOMER_ID), 'X-Signature': signature}


BASE_URL = 'https://api.naver.com'
API_KEY = '0100000000adc996fd9c6660f2496ec0f64a1ce8c5688874b0d0f5074d8f98b0fadd4793b9'
SECRET_KEY = 'AQAAAACtyZb9nGZg8kluwPZKHOjFpb6b54doFnHnBVokUWhNFw=='
CUSTOMER_ID = '1158940'

uri = '/keywordstool'
method = 'GET'
params = {'hintKeywords' : '알루미늄,철', 'showDetail' : 1}
r = requests.get(BASE_URL + uri, params=params, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

# print("response status_code = {}".format(r.status_code))
# print("response body = {}".format(r.json()))
print(r.json())
result = json.loads(r.text)
# print(result)

simple_df = DataFrame(result['keywordList'])
print(simple_df)