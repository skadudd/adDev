import pandas as pd
from konlpy.tag import Okt
from datetime import datetime
from bs4 import BeautifulSoup
import os, re, json, random
from selenium import webdriver as wb
import codecs

def d_make_dic(words) :
    d_tmp = ["@"]
    d_dic = {}

    for word in words :
        d_tmp.append(word)
        if len(d_tmp) < 3 : continue
        if len(d_tmp) > 3 : d_tmp = d_tmp[1:]
        d_set_dic(d_dic, d_tmp)

        if word == "." :
            d_tmp = ["@"]
            continue
    
    return d_dic

def d_set_dic(dic, s3) :
    w1, w2, w3 = s3
    if not w1 in dic : dic[w1] = {}
    if not w2 in dic[w1] : dic[w1][w2] = {}
    if not w3 in dic[w1][w2] : dic[w1][w2][w3] = 0 # 이상징후
    dic[w1][w2][w3] += 1

def d_make_sentence(dic) :
    d_ret = []
    if not "@" in dic : return "no Dic"
    d_top = dic["@"]

    w1 = d_word_choice(d_top)
    w2 = d_word_choice(d_top[w1])

    d_ret.append(w1)
    d_ret.append(w2)

    while True :
        try:
            w3 = d_word_choice(dic[w1][w2])
            print( w3 )
            d_ret.append(w3)
        except Exception as e :
            print("error : ", e)
            break
        
        if w3 == "." : break
        w1, w2 = w2, w3
    d_ret = "".join(d_ret)

    options = wb.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    d_browser = wb.Chrome("./chromedriver", options = options)
    d_browser.get("https://search.naver.com/search.naver?ie=utf8&query=%EB%84%A4%EC%9D%B4%EB%B2%84+%EB%A7%9E%EC%B6%A4%EB%B2%95+%EA%B2%80%EC%82%AC%EA%B8%B0")

    d_browser.implicitly_wait(2)
    d_textfield = d_browser.find_element_by_css_selector("#grammar_checker > div > div.api_cs_wrap > div.check_box > div.text_box._original > div > div.text_area > textarea")
    d_textfield.clear()
    d_textfield.send_keys(d_ret)

    d_browser.implicitly_wait(2)
    d_clicked = d_browser.find_element_by_css_selector("#grammar_checker > div > div.api_cs_wrap > div.check_box > div.text_box._original > div > div.check_info > button")
    d_clicked.click()

    d_browser.implicitly_wait(2)
    d_text = d_browser.find_element_by_css_selector("#grammar_checker > div > div.api_cs_wrap > div.check_box > div.text_box.right._result.result > div > div.text_area > p")

    return d_text.text

def d_word_choice(sel) :
    d_keys = sel.keys()
    return random.choice(list(d_keys))

def ads_create_contents(z_file_text) :
    
    d_dict_file = z_file_path + ( str(z_file_client) + ".json" )

    if not os.path.exists(d_dict_file) :
        d_file_output = codecs.open(z_file_path + z_file_text, "r", encoding = "utf-16")
        soup = BeautifulSoup(d_file_output, "lxml")
            
        body = soup.select_one("body")
        text = body.getText()
        text = text.replace("…", "")

        d_Okt = Okt()
        d_malist = d_Okt.pos(text, norm = True)
        words = []


        for word in d_malist :
            if not word[1] in ["Punctuation"] :
                words.append( word[0] )
            if word[0] == "." :
                words.append( word[0] )
        
        dic = d_make_dic(words)
        json.dump( dic, open(d_dict_file, "w", encoding = "utf-8") )

    else :
        dic = json.load(open(d_dict_file, "r"))

    cnt = int(input("필요한 콘텐츠 수 : "))

    d_save_list = []
    
    for i in range(cnt) :
        d_sentence = d_make_sentence(dic)
        d_save_list.append( d_sentence )
        print(d_sentence)
        print("------------------")


    d_save_dataframe = pd.DataFrame( d_save_list )

    d_save_date = datetime.now()
    d_save_name = z_file_path + str(z_file_client) + "_" + str(d_save_date.hour) + "_" + str(d_save_date.minute) + ".xlsx"
    d_save_dataframe.to_excel(d_save_name, sheet_name = "DATASET", header = ["문장 콘텐츠"])
        

import pymysql
import re

def ads_create_database(file_path) :

    con = pymysql.connect(host="localhost", user="root", passwd="135790", db="adsDB", charset="utf8")
    cursor = con.cursor()

    # DataBase 첫 테이블 생성
    # cursor.execute("CREATE TABLE adsTable (adsId INT(10) NOT NULL AUTO_INCREMENT PRIMARY KEY, adsCategory VARCHAR(3000) NOT NULL, adsCopyright VARCHAR(3000) NOT NULL) CHARACTER SET utf8")
    

    # 데이터 삽입
    # df = pd.read_excel( file_path, "DATASET" )

    # for i in range( len(df) ) :
    #     txt = re.sub('[^A-Za-z0-9가-힣\s]', '', df['콘텐츠 제목'][i])

    #     cursor.execute(" INSERT INTO adsTable VALUES('{}', '{}', '{}') ".format(i+1, "Food_Dining", txt))
    #     print( "전체 {} 개 중, 현재 {} 개 DB INSERT 완료 ..".format(len(df), i+1) )
    # con.commit()


    # 
    sqldf = pd.read_sql("SELECT adsCategory, adsCopyright FROM adsDB.adsTable", con)

    f = open(z_file_path + "max.txt", "w", encoding='utf16')
    
    for i in range( len(sqldf) ) :
        if i == 0 :
            f.write("<body> \n\n")
        else :
            f.write("<p>{}</p> \n".format( sqldf['adsCopyright'][i] ) )

    f.write("\n </body>")
    f.close()

    import time
    time.sleep(1)

    ads_create_contents("max.txt")

if __name__ == "__main__" :

    z_owner_name = "6_my"
    z_owner_code = "078"

    z_file_path = "./Clients/" + z_owner_name + "/" + z_owner_code + "/"
    z_file_client = z_owner_name + "_" + z_owner_code
    z_file_name = z_owner_code + ".xlsx"
    z_file_paths = z_file_path + z_file_name
    z_file_text = "max.txt"

    ads_create_database(z_file_paths)

    # ads_create_contents(z_file_text)