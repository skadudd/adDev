from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium import webdriver as wd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import time
import re
import pandas as pd
import numpy as np
import datetime
import xlsxwriter

def get_param():
    url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=blog&query=&oquery=%ED%8C%8C%EC%9D%B4%EC%8D%AC&tqi=h8CEzsp0JXVssahDcBCssssstXK-464763"
    search_param = input("검색어 입력 : ")
    return url, search_param

def execute_script(order,driver):
    order_result = driver.execute_script(order)
    time.sleep(5)
    return order_result

def scrap_web(url,search_param):
    driver = webdriver.Chrome("./chromedriver")
    driver.get(url)
    search_box = driver.find_element(By.CSS_SELECTOR,'#nx_query')
    search_box.send_keys(search_param)
    #검색어 입력 및 클릭
    search_enter = driver.find_element(By.CSS_SELECTOR,'#nx_search_form > fieldset > button > i')
    search_enter.click()
    driver.maximize_window()
    # driver.implicitly_wait(10)
    get_last_height = "return document.body.scrollHeight"
    do_scroll = "window.scrollTo(0,document.body.scrollHeight);"
    i = 0
    last_height = execute_script(get_last_height,driver)
    
    while True:
        execute_script(do_scroll,driver)
        driver.implicitly_wait(0.1)

        i += 1
        print(i)
        if i == 10:
            new_last_height = execute_script(get_last_height,driver)
            print(new_last_height)
            print(last_height)
            if last_height == new_last_height:
                break
            else:
                last_height = new_last_height
                i = 0
            
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')

    return soup

def parse_text(soup):
    title = soup.select('ul.lst_total>li>div>div>a')
    description = soup.select('ul.lst_total>li>div>div>.total_group>div')
    timestamp = soup.select('ul.lst_total>li>div>div>div>.total_sub>span>span>.etc_dsc_area')
    author = soup.select('ul.lst_total>li>div>div>div>.total_sub>span>span>.etc_dsc_inner>a')

    data = {
        'title' : [title[i].text for i in range(len(title))],
        'description' : [description[i].text for i in range(len(title))],
        'author' : [author[i].text for i in range(len(title))],
        'timestamp' : [timestamp[i].text for i in range(len(title))]
        }
    df = pd.DataFrame(data)
    return df

def export_file(df,search_param):
    writer = pd.ExcelWriter(f"/Users/young/git/project/export/{search_param}_{datetime.datetime.now().strftime('%Y-%m-%d')}.xlsx", engine="xlsxwriter")
    df.to_excel(writer,sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets["Sheet1"]
    writer.save()

def init():
    url, search_param = get_param()
    soup = scrap_web(url,search_param)
    df = parse_text(soup)
    export_file(df,search_param)
    df
    
init()