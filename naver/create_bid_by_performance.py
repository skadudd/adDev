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
request_query_file = '/20212_PC_금속절단_구좌순위별_비딩가.csv'
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
    if x > 50 :
        return '인기'
    else :
        return '비인기'
#분류 1 정규식
def define_regex(x):
    regex = re.compile(r'(절단|워터젯|레이저|레이져|가공$|벤딩$|밴딩$|절곡$|샤링$|판금|커팅|절단)')
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
    regex = re.compile(r'(^대전|^울산|^구로|^서울|^구미|[a-z]|절단기|기$|벤더$|기계$|^목|화분|피규어|가공|사출기|캐드|CAD|^디비디|제품디자인업체|사출|지그|골프채|디자인소품|화장품용기|용기|플라스틱병|장난감|아이디어제품|시작품|프로토타입|IT|휴대폰|핸드폰|아이폰|갤럭시|아이패드|전자|^피규어|안경|애플워치|아이팟|악세서리|악세사리|가구|의자|커틀러리|주변기기|가습기|로봇|마우스|헤드셋|스피커|히터|다리미|면도기|무선|블루투스|레저|낚시|^용품|캠핑|취미|실험|마스크|자동차|산업용품|자재|고양|용인|창원|성남|부천|화성|남양|김해|평택|포항|시흥|파주|의정|김포|양산|원주|진주|세종|광명|아산|익산|춘천|경산|군포|군산|하남|여수|순천|경주|거제|목포|오산|이천|강릉|양주|충주|안성|구리|서산|서귀포|당진|안동|포천|의왕|광양|김천|제천|통영|논산|칠곡|사천|여주|공주|양평|속초|예산|주얼리|쥬얼리|패션|사업|행사|국비지원|POM|메탈$|플라스틱$|실험|와이어|압출|드릴링|휴대폰|양두|황동제작|자동차|항공|비행기|선박|조명|용품$|장비$|선반$|가격$|설계$|탭$|용품$|장비$|부품$|기술$|종류$|머신$|기계$|산업$|GUR$|나일론$|테프론$|아세탈$|티타늄$|네이트$|MDF$)')
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
        #최대 클릭수가 0이 아니며, 최대 비딩가가 4000원 미만일 시, 클릭 변동폭이 가장 높은 구좌 중, 비딩가가 가장 낮은 구좌에 비딩하라.
        elif df['clicks'].max() != 0 and df['bid'].max() < 4000 :
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