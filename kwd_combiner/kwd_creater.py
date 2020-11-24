import time
from datetime import date
import numpy
import math
import time
from pathlib import Path
import pandas as pd
from pandas import DataFrame
import random
from itertools import product

today = date.today()
query = '/Users/maketing/adDev/kwd_combiner/query/query6.csv'
path = '/Users/maketing/adDev/kwd_combiner/created_query'

def get_data():
    df = pd.read_csv(query)
    return df

def nan_finder(kwd):
    if type(kwd) == str:
        return True
    if numpy.isnan(kwd):
        return False

def kwd_attributer(query):
    db = []
    one_list = []
    two_list = []
    three_list = []
    #four_list = []
    #five_list = []

    for v in query['one'] :
        if nan_finder(v) is False :
            one_list.append('')
        else :
            one_list.append(v)

    for v in query['two'] :
        if nan_finder(v) is False :
            two_list.append('')
        else :
            two_list.append(v)

    for v in query['three'] :
        if nan_finder(v) is False :
            three_list.append('')
        else :
            three_list.append(v)

    #for v in query['four'] :
    #    if nan_finder(v) is False :
    #        four_list.append('')
    #    else :
    #        four_list.append(v)
        
    # for v in query['five'] :
    #     if nan_finder(v) is False :
    #         five_list.append('')
    #     else :
    #         five_list.append(v)

    db.append(one_list)
    db.append(two_list)
    db.append(three_list)
    #db.append(four_list)
    #db.append(five_list)

    return db
    print(db )

def delete_duplicate(df):
    deleted_duplicate_data = df.drop_duplicates('kwd')
    return deleted_duplicate_data

def kwd_combine_setter(db):
    df = []
    a = list(product(*db))

    for v in a:
        row = []
        my_lst_str = ''.join(map(str, v))
        row.append(my_lst_str)
        df.append(row)
        row = []
        #print(my_lst_str)
    #print(df)
    data_frame = pd.DataFrame(df)
    data_frame.columns = ['kwd']
    #print(data_frame)
    return data_frame
    
def csv_writer(data,kwd):
    data.to_csv(Path(path, f'{today.year}{today.month}_{kwd}_키워드조합.csv',encoding='utf-8-sig'), index=False)

def init():
    query = get_data()
    kwd = query['one'][0]
    kwd_attributed = kwd_attributer(query)
    kwd_combined = kwd_combine_setter(kwd_attributed)
    deleted_duplicates = delete_duplicate(kwd_combined)
    print(deleted_duplicates)
    csv_writer(deleted_duplicates,kwd)

init()