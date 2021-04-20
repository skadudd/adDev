#! /Users/kim/python
# -*- coding: utf-8 -*-

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
import numpy

import kwd_uploader

today = date.today()
monthly_performance_path = '../kwd_bid_attributer'
request_query_file = '/20213_PC_캐드_구좌순위별_비딩가.csv'
target_dir = '../kwd_bid_attributer'

BASE_URL = 'https://api.naver.com'
API_KEY = '0100000000adc996fd9c6660f2496ec0f64a1ce8c5688874b0d0f5074d8f98b0fadd4793b9'
SECRET_KEY = 'AQAAAACtyZb9nGZg8kluwPZKHOjFpb6b54doFnHnBVokUWhNFw=='
CUSTOMER_ID = '1158940'

def get_header(method, uri, api_key, secret_key, customer_id):
    timestamp = str(round(time.time() * 1000))
    signature = signaturehelper.Signature.generate(timestamp, method, uri, SECRET_KEY)
    return {'Content-Type': 'application/json; charset=UTF-8', 'X-Timestamp': timestamp, 'X-API-KEY': API_KEY, 'X-Customer': str(CUSTOMER_ID), 'X-Signature': signature}



def get_query():
    df = pd.read_csv(monthly_performance_path + request_query_file ,header=None,encoding='utf-8')
    return df

def get_rows(query):
    list_of_rows = []
    list_of_kwds = []
    for num in range(len(query)):
        inner = []

        if num == 0:
            continue
        row = query.iloc[num]
        list_of_kwds.append(row[0])
        row.pop(0)
        for value in row:
            if value.isdigit() == True :
                inner.append(value)
        list_of_rows.append(inner)

    return list_of_kwds,list_of_rows


def get_data(kwd_list, row_list):
    # bids[] : The maximum of 100 bids can be requested at once.
    uri = '/estimate/performance/keyword'
    method = 'POST'
    handled_df = []
    
    for v in range(len(kwd_list)):
        r = requests.post(BASE_URL + uri, json={'device': 'PC', 'keywordplus': True, 'key': kwd_list[v], 'bids':row_list[v] }, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))
        if r.status_code is not 200:
            time.sleep(5)
            r = requests.post(BASE_URL + uri, json={'device': 'PC', 'keywordplus': True, 'key': kwd_list[v], 'bids':row_list[v] }, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))
            print('sleep 5')

        print("response status_code = {}".format(r.status_code))
        json_data = json.loads(r.text)
        df = handle_data(json_data)
        get_best_bid = get_best_performance_bid(df)
        handled_df.append(get_best_bid)        
        #handled_df.append(df)

    return handled_df

def momentom_cal(df):
    names = ['bid','impressions','clicks']
    cal_rows_list = []
    #print(df)
    
    for name in names:
        df = df.fillna(0)
        df = df[df[name] != 0]
        df.tail()
        col_name = name
        arr = []

        pfm_monentom_rate = []
        pfm_range_fct = []
        if range(len(df)) == 0 :
            pfm_monentom_rate = [0,0,0,0,0,0,0,0,0,0]
        else :    
            for v in range(len(df)):
                arr.append(df[col_name][v])

            for v in range(len(arr)):
                #print('식은 : ',arr[v],'','-','',arr[len(arr)-1])
                pfm_monentom_rate.append((arr[v] - arr[len(arr)-1])/arr[len(arr)-1])
                
            if len(pfm_monentom_rate) != 10 :
                while len(pfm_monentom_rate) <= 9:
                    pfm_monentom_rate.append(0)

            #print(pfm_monentom_rate)
        
        for v in range(10):
            inner_cal_list = []
            if v !=9 :
                s = v + 1
                inner_cal_list.append(pfm_monentom_rate[v] - pfm_monentom_rate[s])
                pfm_range_fct.append(inner_cal_list)
            else :
                inner_cal_list.append(pfm_monentom_rate[9])
                pfm_range_fct.append(inner_cal_list)
            
        cal_df = pd.DataFrame(pfm_range_fct)
        cal_df.columns = [name + '_cal']
        cal_rows_list.append(cal_df)

    data_merged = pd.concat([cal_rows_list[0],cal_rows_list[1],cal_rows_list[2]],axis=1)
    
    #print(data_merged)
        
    return data_merged

def handle_data(json_data):
    kwd = json_data['keyword']
    print(kwd)
    rank = pd.Series([1,2,3,4,5,6,7,8,9,10])
    
    df = pd.DataFrame.from_dict(json_data['estimate'])
    df.insert(0,'rank',rank,allow_duplicates = False)
    df.insert(0,'keyword',kwd,allow_duplicates = False)
    df['cpc'] = round(df['cost']/df['clicks'],0)
    monentom_df = momentom_cal(df)
    merged_df = pd.concat([df,monentom_df],axis=1)
    #print(list(merged_df))
    merged_df = merged_df[['keyword','rank','bid','impressions','clicks','cpc','cost','bid_cal','impressions_cal','clicks_cal']]

    return merged_df


def get_best_performance_bid(list_of_df):
    # list_of_df['분류1'] = list_of_df['keyword'].apply(lambda x : define_relation(x))
    # list_of_df['분류2'] = list_of_df['bidding1st'].apply(lambda x : define_popularity(x))
    keyword = list_of_df['keyword'][0]
    impressions = list_of_df['impressions'][0]
    kwd_relationship_score = define_relation(keyword)
    kwd_popularity_score = define_popularity(impressions)
    best_bid = do_math_for_best_bid(list_of_df,kwd_relationship_score,kwd_popularity_score)
    
    return best_bid
    
#분류 1
def define_relation(x):
    r = define_regex(x)
    r2 = define_regex2(x)
    if r ==True and r2 == None :
        return '고관련'
    else :
        return '저관련'

def define_popularity(x):
    if x > 1000 :
        return '인기'
    else :
        return '비인기'
#분류 1 정규식
def define_regex(x):
    regex = re.compile(r'(설계|디자인|도면|기구|제조|제작|생산|모델링|개발|설계|DESIGN)')
    r = regex.search(x)
    print(x,'==',r)
    # return r

    # r = regex.match(x)
    # print('r = ',r)
    if r == None:
        return False
    else :
        return True
#분류 1 정규식
def define_regex2(x):
    regex = re.compile(r'(DXF)')
    r = regex.search(x)
    return r

def do_math_for_best_bid(df,kwd_r_score,kwd_p_score):
    #고관련 인기

    if kwd_r_score == '고관련' and kwd_p_score == '인기' :
        max_click_biddings = df[df['clicks']==df['clicks'].max()]
        #최대 클릭 수가 0이라면 70원에 비딩하라.
        if df['clicks'].max() == 0 :
            best_bid = df[df['rank']==10]
            best_bid['attr'] = '고관련인기'
            return best_bid
        #0이 아니며, 최대 클릭수를 가진 구좌가 중복될때, 최소 비딩가에 비딩하라.
        # elif len(max_click_biddings) >= 2 :
            # best_bid = max_click_biddings[max_click_biddings['bid']==max_click_biddings['bid'].min()]
            # print(best_bid)
        #최대 클릭수가 0이 아니며, 최대 비딩가가 10000원 미만일 시, 클릭 변동폭이 가장 높은 구좌 중, 비딩가가 가장 낮은 구좌에 비딩하라.
        elif df['clicks'].max() != 0 and df['bid'].max() < 10000 :
            max_click_cal = df[df['clicks_cal']==df['clicks_cal'].max()]
            best_bid = max_click_cal[max_click_cal['bid']==max_click_cal['bid'].min()]
            best_bid['attr'] = '고관련인기'
            return best_bid
        #노출 변동폭이 0인 값이 중복될때, 최대 노출값을 가진 구좌들 중 클릭이 1 이상 보장되는 구좌 중 최소 비딩 금액에 비딩하라.
        elif len(df[df['impressions_cal'] == 0]) > 1 :
            max_imp_cal = df[df['impressions']==df['impressions'].max()]
            min_one_click = max_imp_cal[max_imp_cal['clicks']!=0]
            best_bid = min_one_click[min_one_click['bid']==min_one_click['bid'].min()]
            best_bid['attr'] = '고관련인기'
            return best_bid

        
    #고관련 비인기 = 고관련 + 1위 비딩가 150원 이하
    if kwd_r_score == '고관련' and kwd_p_score == '비인기' :
       
        #1~10위 까지 70원 이상의 비딩이 없다면 10위 (70원)으로 비딩하라
        if len(df[df['bid']>70]) == 0 :
            best_bid = df[df['rank']==10]
            best_bid['attr'] = '고관련비인기'
            return best_bid
        #노출이 1 이상인 값이 전혀 없다면, 10위에 비딩하라
        elif len(df[df['impressions']<=1]) == 10 :
            best_bid = df[df['rank']==10]
            best_bid['attr'] = '고관련비인기'
            return best_bid
        #노출이 0이 아닌 값들 중 가장 저렴한 값에 비딩하라.
        else :
            df_not_zero = df[df['impressions'] != 0]
            min_bid = df_not_zero[df_not_zero['bid']==df_not_zero['bid'].min()]
            best_bid = min_bid[min_bid['rank']==min_bid['rank'].max()]
            best_bid['attr'] = '고관련비인기'
            return best_bid
        # else :
        #     best_bid = df[df['rank']==1]
        #     best_bid['attr'] = '고관련비인기'
        #     return best_bid
    #저관련 인기
    if kwd_r_score == '저관련' and kwd_p_score == '인기' :
        #print(df)
        #1~10 순위 중 1000원 이하의 bid가 없다면 10위로 비딩하라
        if len(df[df['bid']<=1000]) == 0 :
            best_bid = df[df['rank']==10]
            best_bid['attr'] = '저관련인기'
            return best_bid
        #노출 변동폭이 0인 값이 중복될때, 최대 노출 구좌들 중 최소 비딩가에 비딩하라.
        elif len(df[df['impressions_cal'] == 0]) > 1 :
            max_imp_cal = df[df['impressions']==df['impressions'].max()]
            best_bid = max_imp_cal[max_imp_cal['bid']==max_imp_cal['bid'].min()]
            best_bid['attr'] = '저관련인기'
            return best_bid
        #1000원 이하의 값이 있다면, 노출 수가 0이 아니며, bid 변동폭이 가장 급격한 구간 바로 아래의 구좌에 비딩하라.
        else :
            df_not_zero = df[df['impressions'] != 0]
            df_momentom = df_not_zero[df_not_zero['bid_cal']==df_not_zero['bid_cal'].max()]
            if len(df_momentom) > 1:
                best_bid = df[df['rank']==df_momentom['rank'].values[0] + 1]
                best_bid['attr'] = '저관련인기'
                return best_bid
            else : 
                best_bid = df_momentom
                best_bid['attr'] = '저관련인기'
                return best_bid
 
    #저관련 비인기
    if kwd_r_score == '저관련' and kwd_p_score == '비인기' :
        #노출이 1 이상인 값이 전혀 없다면, 10위에 비딩하라
        if len(df[df['impressions']<=1]) == 10 :
            best_bid = df[df['rank']==10]
            best_bid['attr'] = '저관련비인기'
            return best_bid
        #노출이 0이 아닌 값들 중 가장 저렴한 값에 비딩하라.
        else :
            df_not_zero = df[df['impressions'] != 0]
            min_bid = df_not_zero[df_not_zero['bid']==df_not_zero['bid'].min()]
            best_bid = min_bid[min_bid['rank']==min_bid['rank'].max()]
            best_bid['attr'] = '저관련비인기'
            return best_bid

def concat_df(data):
    frames = []
    for i in range(len(data)):
        frames.append(data[i])
    result = pd.concat(frames)
    return result

def write_csv(concated_df,kwd):
    concated_df.to_csv(Path(target_dir, f'{today.year}{today.month}_{kwd}_키워드최적비딩가.csv'), index=False)
    #print(concated_df)

def init() :
    DB = []
    query = get_query()
    main_kwd = query[0][1]
    kwd_list,row_list = get_rows(query)
    list_of_df = get_data(kwd_list,row_list)
    concated_df = concat_df(list_of_df)
    concated_df = concated_df.reset_index()
    dropped_df = concated_df.drop_duplicates(['keyword'], keep='first')
    kwd_uploader.create_kwd_set(dropped_df)
    write_csv(dropped_df,main_kwd)
    
init()