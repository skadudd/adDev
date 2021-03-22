import time
import random
import requests

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

uri = '/ncc/keywords'
# uri = '/ncc/adgroups/grp-a001-01-000000018624529/restricted-keywords?type&#x3D;KEYWORD_PLUS_RESTRICT'
method = 'GET'
r = requests.get(BASE_URL + uri, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))
print(r.json())

# ManageCustomerLink Usage Sample

# uri = '/customer-links'
# method = 'GET'
# r = requests.get(BASE_URL + uri, params={'type': 'MYCLIENTS'}, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

# print("response status_code = {}".format(r.status_code))
# print("response body = {}".format(r.json()))


# # BusinessChannel Usage Sample

# uri = '/ncc/channels'
# method = 'GET'
# r = requests.get(BASE_URL + uri, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

# print("response status_code = {}".format(r.status_code))
# print("response body = {}".format(r.json()))


# Campaign test
# uri = '/ncc/campaigns'
# method = 'GET'
# r = requests.get(BASE_URL + uri, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))
# print(type(r))
# target_campaign = r.json()[1]
#print(target_campaign)
# Adgroup Usage Sample

## 1. GET adgroup Usage Sample

# uri = '/ncc/adgroups/grp-a001-01-000000018613590'
# method = 'GET'
# r = requests.get(BASE_URL + uri, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

# print("response status_code = {}".format(r.status_code))
# print("response body = {}".format(r.json()))
# target_adgroup = r.json()
#print(target_adgroup)

# 1. GET adgroup Usage Sample

# uri = '/ncc/ads/nad-a001-01-000000114741459'
# method = 'GET'
# r = requests.get(BASE_URL + uri, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

# print("response status_code = {}".format(r.status_code))
# print("response body = {}".format(r.json()))
# target_adgroup = r.json()
# print(target_adgroup)

# 2. CREATE adgroup Usage Sample

# uri = '/ncc/adgroups'
# method = 'POST'
# payload = {'name': 'TEST#' + str(random.randrange(1000, 9999)), 'nccCampaignId' : 'cmp-a001-01-000000003407888', 'pcChannelId' : 'bsn-a001-00-000000000882190', 'mobileChannelId': 'bsn-a001-00-000000000882190'}
# r = requests.post(BASE_URL + uri, json=payload, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

# print("response status_code = {}".format(r.status_code))
# print("response body = {}".format(r.json()))

# created_adgroup = r.json()
# print(created_adgroup['nccAdgroupId'])

# # 3. UPDATE Adgroup Usage Sample

# uri = '/ncc/adgroups/' + created_adgroup['nccAdgroupId']
# method = 'PUT'
# created_adgroup['userLock'] = 0
# r = requests.put(BASE_URL + uri, params={'fields': 'userLock'}, json=created_adgroup, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

# print("response status_code = {}".format(r.status_code))
# print("response body = {}".format(r.json()))

# # 4. DELETE Adgroup

# uri = '/ncc/adgroups/' + created_adgroup['nccAdgroupId']
# method = 'DELETE'
# r = requests.delete(BASE_URL + uri, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

# print("response status_code = {}".format(r.status_code))
# print("response body = {}".format(r.content))

# # AdKeyword Usage Sample

# 1. CREATE AdKeyword

# uri = '/ncc/keywords'
# method = 'POST'
# r = requests.post(BASE_URL + uri, params={'nccAdgroupId': 'grp-a001-01-000000018602440'}, json=[{'keyword': 'hello'}], headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

# print("response status_code = {}".format(r.status_code))
# print("response body = {}".format(r.json()))

# created_adkeyword = r.json()[0]

# 2. GET AdKeyword

# uri = '/ncc/keywords'
# method = 'GET'
# r = requests.get(BASE_URL + uri, params={'nccAdgroupId': 'grp-a001-01-000000018624529'}, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

# print("response status_code = {}".format(r.status_code))
# # print("response body = {}".format(r.json()))
# r_data = r.json()
# i = 0
# for v in range(len(r_data)):
#     i += 1
#     print(i,'',r_data[v]['nccKeywordId'])

# # 3. UPDATE AdKeyword

# uri = '/ncc/keywords'
# method = 'PUT'
# created_adkeyword['userLock'] = 0
# r = requests.put(BASE_URL + uri, params={'fields': 'userLock'}, json=[created_adkeyword], headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

# print("response status_code = {}".format(r.status_code))
# print("response body = {}".format(r.json()))


# # 4. GET and UPDATE AdKeyword (BidAmt)

# uri = '/ncc/keywords/' + created_adkeyword['nccKeywordId']
# method = 'GET'
# r = requests.get(BASE_URL + uri, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

# print("response status_code = {}".format(r.status_code))
# print("response body = {}".format(r.json()))

# retrieved_adkeyword = r.json()

# uri = '/ncc/keywords'
# method = 'PUT'
# retrieved_adkeyword['bidAmt'] = 300
# retrieved_adkeyword['useGroupBidAmt'] = 0
# r = requests.put(BASE_URL + uri, params={'fields': 'bidAmt'}, json=[retrieved_adkeyword], headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

# print("response status_code = {}".format(r.status_code))
# print("response body = {}".format(r.json()))


# # 5. DELETE AdKeyword

# uri = '/ncc/keywords/' + created_adkeyword['nccKeywordId']
# method = 'DELETE'
# r = requests.delete(BASE_URL + uri, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

# print("response status_code = {}".format(r.status_code))
# print("response body = {}".format(r.content))


# Estimate Usage Sample

# 1. average-position-bid

# uri = '/estimate/average-position-bid/keyword'
# method = 'POST'
# r = requests.post(BASE_URL + uri, json={'device': 'PC', 'items': [{'key': '금속가공', 'position': 7}, {'key': '중고차', 'position': 7}, {'key': '자전거여행', 'position': 9}]}, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

# print("#response status_code = {}".format(r.status_code))
# print("#response body = {}".format(r.json()))


# # 2. exposure-minimum-bid

# uri = '/estimate/exposure-minimum-bid/keyword'
# method = 'POST'
# r = requests.post(BASE_URL + uri, json={'device': 'PC', 'period': 'MONTH', 'items': ['제주여행', '중고차', '자전거여행']}, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

# print("response status_code = {}".format(r.status_code))
# print("response body = {}".format(r.json()))

# 3. median-bid

# uri = '/estimate/median-bid/keyword'
# method = 'POST'
# r = requests.post(BASE_URL + uri, json={'device': 'PC', 'period': 'MONTH', 'items': ['금속가공', '중고차', '자전거여행']}, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

# print("response status_code = {}".format(r.status_code))
# print("response body = {}".format(r.json()))


# # 4. performance

# uri = '/estimate/performance/keyword'
# method = 'POST'
# r = requests.post(BASE_URL + uri, json={'device': 'PC', 'keywordplus': True, 'key': '중고차', 'bids': [100, 500, 1000, 1500, 2000, 3000, 5000]}, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

# print("response status_code = {}".format(r.status_code))
# print("response body = {}".format(r.json()))

# # 5. performance-bulk

# uri = '/estimate/performance-bulk'
# method = 'POST'
# r = requests.post(BASE_URL + uri, json={'items': [{'device': 'PC', 'keywordplus': True, 'keyword': '제주여행', 'bid': 70}, {'device': 'PC', 'keywordplus': True, 'keyword': '제주도', 'bid': 80}, {'device': 'PC', 'keywordplus': True, 'keyword': '제주도맛집', 'bid': 90}, ]}, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

# print("response status_code = {}".format(r.status_code))
# print("response body = {}".format(r.json()))

# Stat Usage Sample

# 1. GET Summary Report per multiple entities 

# uri = '/stats'
# method = 'GET'
# #stat_ids = [target_adgroup['nccCampaignId'], target_adgroup['nccAdgroupId']]
# stat_ids = ['cmp-a001-01-000000002310963','cmp-a001-01-000000003098423','cmp-a001-01-000000003098427']
# r = requests.get(BASE_URL + uri, params={'ids': stat_ids, 'fields': '["clkCnt","impCnt","salesAmt", "ctr", "cpc", "avgRnk", "ccnt"]', 'timeRange': '{"since":"2020-09-01","until":"2020-09-25"}'}, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

# print("response status_code = {}".format(r.status_code))
# print("response body = {}".format(r.json()))

# #판다스
# fields=r.json()['data'][0].keys()
# df=DataFrame(None,columns=fields)

# for idx in range(0,len(r.json()['data'])):
#     df=df.append(DataFrame(r.json()['data'][idx],index=[idx]))

# df.set_index('id',inplace=True)
# df.rename({'ctr':'클릭률','clkCnt':'클릭수','cpc':'평균클릭비용','ccnt':'전환수','avgRnk':'평균노출순위','impCnt':'노출수','salesAmt':'총비용'},axis=1,inplace=True)
# df=df[['노출수', '클릭수', '클릭률', '평균클릭비용', '총비용','전환수', '평균노출순위']]


#df.to_excel('result.xlsx')