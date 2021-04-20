import os
import time
import shutil
import random
import json
import glob
import requests
import signaturehelper
import pandas as pd
from pandas import DataFrame
from pathlib import Path
import csv
from dateutil import rrule
from datetime import datetime, timedelta
from dateutil.parser import *

BASE_URL = 'https://api.naver.com'
API_KEY = '0100000000adc996fd9c6660f2496ec0f64a1ce8c5688874b0d0f5074d8f98b0fadd4793b9'
SECRET_KEY = 'AQAAAACtyZb9nGZg8kluwPZKHOjFpb6b54doFnHnBVokUWhNFw=='
CUSTOMER_ID = '1158940'
input_file = '../DB_for_GA_naver/'
output_file = '../DB_of_naver_combined/'
campaignList = ['cmp-a001-01-000000003407889',
                'cmp-a001-01-000000003407888',
                'cmp-a001-01-000000003645640',
                'cmp-a001-01-000000003605317',
                'cmp-a001-01-000000003711127',
                'cmp-a001-01-000000003711121',
                'cmp-a001-01-000000003707633',
                'cmp-a001-01-000000003707625',
                'cmp-a001-01-000000003865318',
                'cmp-a001-01-000000003865902',
                'cmp-a001-04-000000003747667',
                'cmp-a001-01-000000003991616'
                ]

#1. GET Summary Report per multiple entities 
input_start_date = input('보고 시작 날짜 : ')
input_end_date = input('보고 종료 날짜 : ')

start_date = parse(input_start_date)
end_date = parse(input_end_date)

#import key
def get_header(method, uri, api_key, secret_key, customer_id):
    timestamp = str(round(time.time() * 1000))
    signature = signaturehelper.Signature.generate(timestamp, method, uri, SECRET_KEY)
    return {'Content-Type': 'application/json; charset=UTF-8', 'X-Timestamp': timestamp, 'X-API-KEY': API_KEY, 'X-Customer': str(CUSTOMER_ID), 'X-Signature': signature}

def iterate_request():
    for dt in rrule.rrule(rrule.DAILY, dtstart=start_date, until=end_date):
        date = str(dt.date())
        try : 
            data_to_csv(date)
        except : 
            print(f'no data in {date}')

#requested data to csv
def data_to_csv(date):
    for v in campaignList :
        uri = '/stats'
        method = 'GET'
        rangeOftime = {"since" : date, "until" : date}
        json_range_of_time = json.dumps(rangeOftime, indent=2)
        stat_ids = [v]
        params={
            'ids': stat_ids,
            'fields': '["clkCnt","impCnt","salesAmt"]', 
            'timeRange': json_range_of_time }
        r = requests.get(BASE_URL + uri, params, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))
        # print("response status_code = {}".format(r.status_code))
        # print("response body = {}".format(r.json()))
        json_data = json.loads(r.text)

        if(len(json_data['data']) == 0) :
            print(f'no data in {v} on {date}')
            continue
        
        data = json_data['data'][0]

        print(v)
        print('campaign : ',data)
        striped_date = date.replace('-','')
        medium = 'cpc'
        source = 'search.naver.com'
        clkCnt = data['clkCnt']
        impCnt = data['impCnt']
        salesAmt = data['salesAmt']
        campaign = 0

        if(v == 'cmp-a001-01-000000003407889') :
            campaign = 'NSA_cnc_contents'
        elif(v == 'cmp-a001-01-000000003407888') :
            campaign = 'NSA_cnc'
        elif(v == 'cmp-a001-01-000000003707625') :
            campaign = 'NSA_cnc_Mobile'
        elif(v == 'cmp-a001-01-000000003645640') :
            campaign = 'NSA_3dp'
        elif(v == 'cmp-a001-01-000000003707633') :
            campaign = 'NSA_3dp_Mobile'
        elif(v == 'cmp-a001-01-000000003711121') :
            campaign = 'NSA_INJ'
        elif(v == 'cmp-a001-01-000000003711127') : 
            campaign = 'NSA_INJ_Mobile'
        elif(v == 'cmp-a001-01-000000003865318') :
            campaign = 'NSA_SHT'
        elif(v == 'cmp-a001-01-000000003991616') :
            campaign = "NSA_DSN"
        elif(v == 'cmp-a001-01-000000003865902') :
            campaign = 'NSA_SHT_Mobile'
        elif(v == 'cmp-a001-04-000000003747667') :
            campaign = 'NSA_Brand_Search'
        elif(v == 'cmp-a001-01-000000003605317') :
            campaign = 'NSA_Brand'

        newRow = [striped_date, medium, source, clkCnt, salesAmt, impCnt, campaign]
        ad_data = {'ga:date':[striped_date], 'ga:medium':[medium], 'ga:source':[source], 'ga:adClicks':[clkCnt], 'ga:adCost':[salesAmt], 'ga:impressions':[impCnt], 'ga:campaign':[campaign] }
        df = pd.DataFrame(data=ad_data)
        
        df.to_csv(Path(input_file, f'{striped_date} {source} {campaign}.csv'), index=False)

def merge_csv(): 
    allFile_list = glob.glob(os.path.join(input_file, '*.csv'))
    all_data = []

    for file in allFile_list:
        df = pd.read_csv(file)
        all_data.append(df)

    data_combine = pd.concat(all_data, axis=0, ignore_index=True)
    data_combine.to_csv(Path(output_file, f'{start_date.date()}_{end_date.date()}_combined.csv'), index=False )

def removeAllFile():
    if os.path.exists(input_file):
        for file in os.scandir(input_file):
            os.remove(file.path)
        return 'input 폴더 삭제 완료'
    else :
        return 'input 폴더 에러'

def init():
    iterate_request()
    merge_csv()
    removeAllFile()

init()