import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import time
from datetime import date
import random
import requests
import signaturehelper
import pandas as pd
from pathlib import Path
from pandas import DataFrame

high_scored_keywords = []

def get_header(method, uri, api_key, secret_key, customer_id):
    timestamp = str(round(time.time() * 1000))
    signature = signaturehelper.Signature.generate(timestamp, method, uri, SECRET_KEY)
    return {'Content-Type': 'application/json; charset=UTF-8', 'X-Timestamp': timestamp, 'X-API-KEY': API_KEY, 'X-Customer': str(CUSTOMER_ID), 'X-Signature': signature}

BASE_URL = 'https://api.naver.com'
API_KEY = '0100000000adc996fd9c6660f2496ec0f64a1ce8c5688874b0d0f5074d8f98b0fadd4793b9'
SECRET_KEY = 'AQAAAACtyZb9nGZg8kluwPZKHOjFpb6b54doFnHnBVokUWhNFw=='
CUSTOMER_ID = '1158940'

def request_to_naver(*args):
    uri = f'/ncc/{args[0]}'
    method = args[1]
    pass
    if len(args) == 4 :
        r = requests.get(BASE_URL + uri, params={args[2]: args[3]}, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))
    else :
        r = requests.get(BASE_URL + uri, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))
    
    print("response status_code = {}".format(r.status_code))
    return r

def get_all_groups():
    # uri_param = 'adgroups'+'{?'+campaign_id+'}'
    uri_param = 'adgroups'
    method_param = 'GET'
    r = request_to_naver(uri_param,method_param)
    if r.status_code is not 200:
        time.sleep(5)
        r = request_to_naver(uri_param,method_param)
    group_list = r.json()

    return group_list

def get_campaign_list():
    uri_param = 'campaigns'
    method_param = 'GET'
    r = request_to_naver(uri_param,method_param)
    # uri = '/ncc/campaigns'
    # method = 'GET'
    # r = requests.get(BASE_URL + uri, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))
    # print(type(r))

    for v in r.json() :
        if v['userLock'] == False :
            campaign_name = v['name']
            campaign_id = v['nccCampaignId']
            if '브' in campaign_name or '고성과' in campaign_name or 'Mobile' in campaign_name :
                continue
            print('moving ',campaign_name)
            move_highscore_kwd(v)
            

def move_highscore_kwd(v) :
    campaign_id = v['nccCampaignId']
    campaign = v['name']
    for group in group_list :
        if group['nccCampaignId'] == campaign_id :
        
            get_keywords(group,campaign)
            # print(high_scored_keywords)
                

def get_keywords(group,campaign):
    gid = group['nccAdgroupId']
    uri_param = 'keywords'
    method_param = 'GET'
    r = request_to_naver(uri_param,method_param,'nccAdgroupId',gid)
    # print(r.json())
    for v in r.json() :
        cell = []
        keyword_id = v['nccKeywordId']
        # print(v['keyword'])
        data = get_stat(keyword_id)
        if data != None :
            print(v['keyword'])
            cell.append(campaign)
            cell.append(group['name'])
            cell.append(v['keyword'])
            cell.append(data)
            # set_keywords_paused(keyword_id)
            high_scored_keywords.append(cell)
    df = pd.DataFrame(high_scored_keywords)
    return

def get_stat(keyword_id) :
    uri = '/stats'
    method = 'GET'
    stat_id = [keyword_id]
    r = requests.get(BASE_URL + uri, params={'id': stat_id, 'fields': '["ccnt"]', 'timeRange': '{"since":"2021-01-04","until":"2021-04-04"}'}, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))
    if r.status_code is not 200:
        time.sleep(5)
        r = requests.get(BASE_URL + uri, params={'id': stat_id, 'fields': '["ccnt"]', 'timeRange': '{"since":"2021-01-04","until":"2021-04-04"}'}, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))
    # print(r.json())
    datas = r.json()['data']
    
    # for v in datas :
    #     ccnt_num += v['ccnt']
    ret = next((index for (index, item) in enumerate(datas) if item['ccnt'] > 0), None)
    if ret != None :
        sum_ccnt = []
        for v in datas :
            sum_ccnt.append(v['ccnt'])
        ccnt_num = sum(sum_ccnt)

        return ccnt_num
    else :
        return None

def write_csv():
    target_dir = ('/Users/kim/Desktop')
    today = date.today()
    df = pd.DataFrame(high_scored_keywords)
    df.to_csv(Path(target_dir, f'{today.year}{today.month}_네이버검색광고_전환키워드.csv'), index=False)

# def set_keywords_paused(keyword_id) :
#     uri = 'ncc/keywords'
#     method = 'PUT'
#     r = requests.put(BASE_URL + uri, params={'nccKeywordId' : keyword_id, 'userLock' : True}, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

# r = requests.get(BASE_URL + uri, params={'nccAdgroupId': 'grp-a001-01-000000018624529'}, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))
def init():
    
    global group_list
    group_list = get_all_groups()
    get_campaign_list()
    write_csv()

init()
    