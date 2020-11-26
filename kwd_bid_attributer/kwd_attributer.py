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
from create_bid_by_performance import *

#query = '/Users/maketing/adDev/kwd_bid_attributer/2020_11_최종키워드소스.csv'
#csv = pd.read_csv(query)

query = pd.read_csv('/Users/maketing/adDev/kwd_bid_attributer/2020_11_최종키워드소스 복사본.csv',header=None)
a = create_bid_by_performance.init(query)
print(a)


# #### 어트리뷰터
# #분류 2
# def define_popularity(x):
#     if x > 70 :
#         return '인기'
#     else :
#         return '비인기'

# #분류 1 정규식
# def define_regex(x):
#     regex = re.compile(r'(CNC|가공$|선반$|업체$|가공$|제작공장$|생산공장$|가공공장|견적$|업체$|파트너$|견적$|단가$|가공|부품|제조|밀링|선반|커팅|컷팅|생산|절삭|목업|제작$|가공단가$|임가공$|설계$)')
#     r = regex.search(x)
#     return r
# #분류 1 정규식
# def define_regex2(x):
#     regex = re.compile(r'(POM|메탈$|플라스틱$|실험|와이어|압출|드릴링|휴대폰|양두|황동제작|자동차|항공|비행기|선박|조명|용품$|장비$|선반$|가격$|설계$|탭$|용품$|장비$|부품$|기술$|종류$|머신$|기계$|산업$|GUR$|나일론$|테프론$|아세탈$|티타늄$|네이트$|MDF$)')
#     r = regex.search(x)
#     return r

# #분류 1
# def define_relation(x):
#     r = define_regex(x)
#     r2 = define_regex2(x)
#     if r != None and r2 == None :
#         return '고관련'
#     else :
#         return '저관련'

# csv['분류1'] = csv['keyword'].apply(lambda x : define_relation(x))
# csv['분류2'] = csv['bidding1st'].apply(lambda x : define_popularity(x))

# print(csv)
# #csv.to_csv(Path('/Users/maketing/adDev/kwd_bid_attributer', '분류_키워드.csv'), index=False)


