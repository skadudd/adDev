import os
import time
import shutil
import random
import json
import glob
import requests
import openpyxl
import signaturehelper
import pandas as pd
from pandas import DataFrame
from pathlib import Path
import csv
from dateutil import rrule
from datetime import datetime, timedelta
from functools import reduce
import re

today = date.today()
monthly_performance_path = '/Users/maketing/adDev/NSA_rel_keyword/monthly_performance_raw_data'
request_query_file = '/202011_CNC_구좌순위별_비딩가.csv'
target_dir = '/Users/maketing/adDev/NSA_rel_keyword/estimate_performance'


BASE_URL = 'https://api.naver.com'
API_KEY = '0100000000adc996fd9c6660f2496ec0f64a1ce8c5688874b0d0f5074d8f98b0fadd4793b9'
SECRET_KEY = 'AQAAAACtyZb9nGZg8kluwPZKHOjFpb6b54doFnHnBVokUWhNFw=='
CUSTOMER_ID = '1158940'

def get_header(method, uri, api_key, secret_key, customer_id):
    timestamp = str(round(time.time() * 1000))
    signature = signaturehelper.Signature.generate(timestamp, method, uri, SECRET_KEY)
    return {'Content-Type': 'application/json; charset=UTF-8', 'X-Timestamp': timestamp, 'X-API-KEY': API_KEY, 'X-Customer': str(CUSTOMER_ID), 'X-Signature': signature}


query = '/Users/maketing/adDev/kwd_bid_attributer/2020_11_최종키워드소스.csv'
csv = pd.read_csv(query)

#### 어트리뷰터
#분류 2
def define_popularity(x):
    if x > 70 :
        return '인기'
    else :
        return '비인기'

#분류 1 정규식
def define_regex(x):
    regex = re.compile(r'(CNC|가공$|선반$|업체$|가공$|제작공장$|생산공장$|가공공장|견적$|업체$|파트너$|견적$|단가$|가공|부품|제조|밀링|선반|커팅|컷팅|생산|절삭|목업|제작$|가공단가$|임가공$|설계$)')
    r = regex.search(x)
    return r
#분류 1 정규식
def define_regex2(x):
    regex = re.compile(r'(POM|메탈$|플라스틱$|실험|와이어|압출|드릴링|휴대폰|양두|황동제작|자동차|항공|비행기|선박|조명|용품$|장비$|선반$|가격$|설계$|탭$|용품$|장비$|부품$|기술$|종류$|머신$|기계$|산업$|GUR$|나일론$|테프론$|아세탈$|티타늄$|네이트$|MDF$)')
    r = regex.search(x)
    return r

#분류 1
def define_relation(x):
    r = define_regex(x)
    r2 = define_regex2(x)
    if r != None and r2 == None :
        return '고관련'
    else :
        return '저관련'

csv['분류1'] = csv['keyword'].apply(lambda x : define_relation(x))
csv['분류2'] = csv['bidding1st'].apply(lambda x : define_popularity(x))

print(csv)
#csv.to_csv(Path('/Users/maketing/adDev/kwd_bid_attributer', '분류_키워드.csv'), index=False)


