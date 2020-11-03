import time
import random
import requests
import openpyxl
import signaturehelper
import pandas as pd
from pandas import DataFrame
import csv
import json

def get_header(method, uri, api_key, secret_key, customer_id):
    timestamp = str(round(time.time() * 1000))
    signature = signaturehelper.Signature.generate(timestamp, method, uri, SECRET_KEY)
    return {'Content-Type': 'application/json; charset=UTF-8', 'X-Timestamp': timestamp, 'X-API-KEY': API_KEY, 'X-Customer': str(CUSTOMER_ID), 'X-Signature': signature}


BASE_URL = 'https://api.naver.com'
API_KEY = '0100000000adc996fd9c6660f2496ec0f64a1ce8c5688874b0d0f5074d8f98b0fadd4793b9'
SECRET_KEY = 'AQAAAACtyZb9nGZg8kluwPZKHOjFpb6b54doFnHnBVokUWhNFw=='
CUSTOMER_ID = '1158940'


#1. GET Summary Report per multiple entities 

uri = '/stats'
method = 'GET'
date = '2020-10-19'

rangeOftime = {"since" : date, "until" : date}
json_range_of_time = json.dumps(rangeOftime, indent=2)

stat_ids = ['cmp-a001-01-000000003407888']
params={
    'ids': stat_ids,
    'fields': '["clkCnt","impCnt","salesAmt"]', 
    'timeRange': json_range_of_time }


#request API
r = requests.get(BASE_URL + uri, params, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

#print("response status_code = {}".format(r.status_code))
#print("response body = {}".format(r.json()))

json_data = json.loads(r.text)
data = json_data['data'][0]

medium = 'cpc'
source = 'search.naver.com'
clkCnt = data['clkCnt']
impCnt = data['impCnt']
salesAmt = data['salesAmt']
campaign = 'NCR_CNC_효율_2'

newRow = [date, medium, source, clkCnt, salesAmt, impCnt, campaign]
d = {'ga:date':[date], 'ga:medium':[medium], 'ga:source':[source], 'ga:adClicks':[clkCnt], 'ga:adCost':[salesAmt], 'ga:impressions':[impCnt], 'ga:campaign':[campaign] }
df = pd.DataFrame(data=d)

df.to_csv(date + source + '.csv', header=1, mode='w')
