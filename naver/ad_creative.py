import time
import random
import requests
import signaturehelper
import pandas as pd
from pandas import DataFrame

# CAPA는 무료! 대기업 {keyword:제조} 파트너들의 견적을 받고 비교해 보세요.
# 여러 업체의 {keyword:제조} 가공 견적, capa에서 한번에 받아보고 비교하세요
# {keyword:제조} 업체 찾지말고, CAPA에서 한번에 받아보고 비교하세요!

def get_header(method, uri, api_key, secret_key, customer_id):
    timestamp = str(round(time.time() * 1000))
    signature = signaturehelper.Signature.generate(timestamp, method, uri, SECRET_KEY)
    return {'Content-Type': 'application/json; charset=UTF-8', 'X-Timestamp': timestamp, 'X-API-KEY': API_KEY, 'X-Customer': str(CUSTOMER_ID), 'X-Signature': signature}


BASE_URL = 'https://api.naver.com'
API_KEY = '0100000000adc996fd9c6660f2496ec0f64a1ce8c5688874b0d0f5074d8f98b0fadd4793b9'
SECRET_KEY = 'AQAAAACtyZb9nGZg8kluwPZKHOjFpb6b54doFnHnBVokUWhNFw=='
CUSTOMER_ID = '1158940'

group_ids = [
    "grp-a001-01-000000020586373",
    "grp-a001-01-000000020586372",
    "grp-a001-01-000000020586375",
    "grp-a001-01-000000020586374"
]
for v in group_ids:
    print(v)

for v in group_ids : 
    uri = '/ncc/ads'
    method = 'POST'
    payload = {
    "ad" : {
    "pc": {"final": "https://capa.ai"},
    "mobile": {"final": "https://capa.ai"},
    "headline": "제조 견적비교 서비스, 카파",
    "description": "CAPA는 무료! 대기업 {keyword:제조} 파트너들의 견적을 받고 비교해 보세요."},
    "type" : 'TEXT_45',
    "nccAdgroupId" : v
    }
    r = requests.post(BASE_URL + uri, json=payload, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

    print("response status_code = {}".format(r.status_code))
    print("response body = {}".format(r.json()))

    created_adgroup = r.json()
