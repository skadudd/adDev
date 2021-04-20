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
campaign = {
    "cnc" : "cmp-a001-01-000000003407888",
    "3dp" : "cmp-a001-01-000000003645640",
    "inj" : "cmp-a001-01-000000003711121",
    "sht" : "cmp-a001-01-000000003865318"
    }
group_cnc = [
"기술_공법_방식",
"기술_목적_범용",
"기술_목적_산업",
"기술_목적_소재_금속",
"기술_목적_소재_기타",
"기술_목적_소재_플라스틱",
"비용",
"생산_서비스",
"생산_서비스_졸업작품",
"생산_아이템_공업품",
"생산_아이템_모형",
"생산_아이템_소품",
"생산_아이템_시제품",
"생산_아이템_아이디어",
"생산_아이템_예술",
"업체_경쟁사",
"업체_범용_서비스",
"업체_제조_서비스",
"업체_지역",
"업체_지원사업"
]
group_3dp = [
"기술_공법_방식",
"기술_목적_범용",
"기술_목적_산업",
"기술_목적_소재_금속",
"기술_목적_소재_기타",
"기술_목적_소재_플라스틱",
"비용",
"생산_서비스",
"생산_서비스_졸업작품",
"생산_아이템_공업품",
"생산_아이템_모형",
"생산_아이템_소품",
"생산_아이템_시제품",
"생산_아이템_아이디어",
"생산_아이템_예술",
"업체_경쟁사",
"업체_범용_서비스",
"업체_제조_서비스",
"업체_지역",
"업체_지원사업"
]
group_inj = [
"기술_공법",
"기술_공법_특수",
"기술_목적_산업",
"기술_목적_산업_설계",
"기술_목적_소량생산",
"기술_소재_산업_플라스틱",
"비용",
"생산_아이템_공업품",
"생산_아이템_산업부품",
"생산_아이템_소품",
"생산_아이템_용기",
"생산_아이템_중장비",
"생산_아이템_IOT",
"생산_일반",
"업체_범용_서비스",
"업체_아이템_금속",
"업체_아이템_플라스틱",
"업체_제조_금형공장",
"업체_제조_서비스",
"업체_지역"
]
group_sht = [
"기술_공법_레이저",
"기술_공법_범용",
"기술_공법_워터젯",
"기술_공법_절곡",
"기술_공법_절단",
"기술_공법_후가공",
"기술_목적_산업",
"기술_소재_산업_동",
"기술_소재_산업_알루미늄",
"기술_소재_산업_철",
"기술_소재_산업_플라스틱",
"비용",
"생산_아이템_기초재료",
"생산_아이템_산업부품",
"생산_아이템_소재",
"생산_아이템_인테리어",
"생산_아이템_프레임",
"업체_공법_범용",
"업체_공법_워터젯",
"업체_공법_프레스",
"업체_범용",
"업체_소재_금속",
"업체_소재_플라스틱",
"업체_지역"
]

def adGroup_creator() :
    for v in group_sht :
        uri = '/ncc/adgroups'
        method = 'POST'
        payload = {
            'name': v, 
            'nccCampaignId' : 'cmp-a001-01-000000003865318', 
            'pcChannelId' : 'bsn-a001-00-000000004519293',
            'mobileChannelId': 'bsn-a001-00-000000004519293',
            'userLock': True
            }
        r = requests.post(BASE_URL + uri, json=payload, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

    #print("response status_code = {}".format(r.status_code))
    #print("response body = {}".format(r.json()))

    created_adgroup = r.json()
    print(created_adgroup)


adGroup_creator()