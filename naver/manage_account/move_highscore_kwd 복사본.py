import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
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

def request_to_naver(*args):
    uri = f'/ncc/{args[0]}'
    method = args[1]
    pass
    if len(args) == 3 :
        r = requests.get(BASE_URL + uri, params={'nccAdgroupId': args[2]}, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))
    else :
        r = requests.get(BASE_URL + uri, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))
    
    print("response status_code = {}".format(r.status_code))
    return r

def get_all_groups():
    # uri_param = 'adgroups'+'{?'+campaign_id+'}'
    uri_param = 'adgroups'
    method_param = 'GET'
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
            move_highscore_kwd(campaign_id)

def move_highscore_kwd(campaign_id) :
    for group in group_list :
        if group['nccCampaignId'] == campaign_id :
            print(group['name'])
            # get_keywords(group['nccAdgroupId'])
            gid = group['nccAdgroupId']
            print(gid)
            get_keywords(gid)

def get_keywords(gid):
    uri_param = 'keywords'
    method_param = 'GET'
    r = request_to_naver(uri_param,method_param,gid)
    çprint(r.json())
# r = requests.get(BASE_URL + uri, params={'nccAdgroupId': 'grp-a001-01-000000018624529'}, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))
def init():
    global group_list
    group_list = get_all_groups()
    get_campaign_list()

init()
    