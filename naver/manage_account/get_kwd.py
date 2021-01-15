import time
import random
import requests
import signaturehelper
import pandas as pd
from pandas import DataFrame

#네이버 키워드 업데이터
#1. 캠페인 내 라이브되고 있는 키워드 데이터를 그룹별로 받는다.
#2. 키워드별 퍼포먼스를 받는다.
#3. 키워드별 estimate
#4. 키워드 bid 업데이트

current_groups = {
    '3dp_pc_related_popular' : {},
    '3dp_pc_related_unpopular' : {},
    '3dp_pc_notRelated' : {},
    'cnc_pc_related' : {},
    'cnc_pc_related' : {},
    'INJ_pc_related' : {},
    'INJ_pc_related' : {},
    '3dp_mobile_related' : {},
    '3dp_mobile_related' : {},
    'cnc_mobile_related' : {},
    'cnc_mobile_related' : {},
    'INJ_mobile_related' : {},
    'INJ_mobile_related' : {}
}

def get_header(method, uri, api_key, secret_key, customer_id):
    timestamp = str(round(time.time() * 1000))
    signature = signaturehelper.Signature.generate(timestamp, method, uri, SECRET_KEY)
    return {'Content-Type': 'application/json; charset=UTF-8', 'X-Timestamp': timestamp, 'X-API-KEY': API_KEY, 'X-Customer': str(CUSTOMER_ID), 'X-Signature': signature}

BASE_URL = 'https://api.naver.com'
API_KEY = '0100000000adc996fd9c6660f2496ec0f64a1ce8c5688874b0d0f5074d8f98b0fadd4793b9'
SECRET_KEY = 'AQAAAACtyZb9nGZg8kluwPZKHOjFpb6b54doFnHnBVokUWhNFw=='
CUSTOMER_ID = '1158940'

def get_keyword():
    uri = '/ncc/keywords'
    method = 'GET'
    r = requests.get(BASE_URL + uri, params={'nccAdgroupId': 'grp-a001-01-000000018624529'}, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))
    print("response status_code = {}".format(r.status_code))
    # print("response body = {}".format(r.json()))
    r_data = r.json()
    return r_data

def set_data_frame(data)
    data = pd.DataFrame(r_data)

def init():
    data = get_keyword()
    set_data_frame(data)

'''
keyword response
[{
    ‘nccKeywordId': 'nkw-a001-01-000003327942573', 
    'keyword': '플라스틱MCT가공견적', 
    'customerId': 1158940, 
    'nccAdgroupId': 'grp-a001-01-000000018624529', 
    'nccCampaignId': 'cmp-a001-01-000000003407888', 
    'links': {'pc': {'final': 'https://capa.ai'}, 
    'mobile': {'final': 'https://capa.ai'}}, 
    'userLock': False, 
    'inspectStatus': 'APPROVED', 
    'bidAmt': 70, 
    'useGroupBidAmt': False, 
    'delFlag': False, 
    'regTm': '2020-12-02T08:25:26.000Z', 
    'editTm': '2020-12-02T08:25:33.000Z', 
    'status': 'ELIGIBLE', 
    'statusReason': 'ELIGIBLE', 
    'nccQi': {'qiGrade': 4}
    }]
'''