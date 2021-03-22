import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from pathlib import Path
import pandas as pd
import re


def scroll_downer(driver):
    last_height = 0
    SCROLL_PAUSE_TIME = 1
 
    while True:
        # 화면 최하단으로 스크롤 다운
        #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
        # 페이지 로드를 기다림
        time.sleep(SCROLL_PAUSE_TIME)
        # element = driver.find_element_by_link_text("crowdy-btn-01")
        element = driver.find_element_by_xpath("//font[text()='종료된 프로젝트 더보기']")
        
        driver.execute_script("arguments[0].scrollIntoView();",element)
        driver.execute_script("arguments[0].click();", element)
        #driver.execute_script("window.scrollTo(0, document.body.scrollHeight-50);")
        time.sleep(SCROLL_PAUSE_TIME)
    
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
    
        # 새로운 높이가 이전 높이와 변하지 않았을 경우 스크롤 종료
        if new_height == last_height:
            break
            # while True:
            #     time.sleep(SCROLL_PAUSE_TIME)
            #     element = driver.find_element_by_xpath("//font[text()='종료된 프로젝트 더보기']")

            #     driver.execute_script("arguments[0].scrollIntoView();",element)
            #     driver.execute_script("arguments[0].click();", element)
            #     #driver.execute_script("window.scrollTo(0, document.body.scrollHeight-50);")
            #     time.sleep(SCROLL_PAUSE_TIME)

            #     # Calculate new scroll height and compare with last scroll height
            #     new_height = driver.execute_script("return document.body.scrollHeight")
            #     if new_height == last_height:
            #         break
        # 스크롤 다운이 된다면 스크롤 다운이 된 후의 창 높이를 새로운 높이로 갱신
        last_height = new_height

def strip_empty_space(text):
    text_sub = re.sub(r"\s", "", text)

    return text_sub

def get_infos(url,driver):
    row = []

    print('scrapping...',url)
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')
    
    # project_title = 
    try:
        close_date = soup.select_one('div.reward-info-box > div.mt5 > span.reward-info-goal').get_text()
    except :
        close_date = "종료"
    achievement_rate = soup.select_one('div.reward-info-box > div.mt20 > span.reward-info-now').get_text()
    total_funded = soup.select_one('div.reward-info-box > div.reward-info-amount')
    extract_sibling = total_funded.span.extract()
    total_funded_extracted = strip_empty_space(total_funded.get_text())
    total_supporters = soup.select('div.reward-info-box > div.mt5')[1].select_one('span.reward-info-now').get_text()
    contact_infos = soup.select('div#profileModal > div.modal-dialog > div.modal-content > div.modal-padding > div.reward-policy-profilebox-1 > div')[1]
    company = contact_infos.select_one('div.reward-info-projectName').get_text()
    email = contact_infos.select_one('a.reward-policy-email').get_text()
    project_name = soup.select_one('div.reward_title').get_text()
    category = 'none'
    phone = 'none'

    print(close_date)
    print(achievement_rate)
    print(total_funded_extracted)
    print(total_supporters)
    print(company)
    print(email)
    print(project_name)

    row.extend((
        category,
        project_name,
        company,
        email,
        phone,
        close_date,
        achievement_rate,
        total_funded_extracted,
        total_supporters
    ))

    return row

def get_campaign_paths(driver):
    paths = []
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')
    test = soup.select('div.col-sm-4')

    for v in range(len(test)):
        link = test[v].find('a')['href']
        print(link)
        paths.append(link)

    return paths

def write_csv(df):
    df.to_csv(Path('/Users/kim/Desktop','crowdy_closed.csv'))

def init():
    raw_data = []
    driver = webdriver.Chrome('/Users/kim/Downloads/chromedriver')
    driver.implicitly_wait(1) 
    driver.get('https://www.ycrowdy.com/reward/list')
    scroll_downer(driver)
    paths = get_campaign_paths(driver)
    print(paths)
    
    for v in paths:
        if v == 'javascript:void(0)':
            print(f'**invalid url...{v}')
            continue
        print(f'valid url...{v}')
        url = 'https://www.ycrowdy.com' + v
        row = get_infos(url,driver)
        if row != None:
            raw_data.append(row)
        else:
            continue

    df = pd.DataFrame(raw_data)
    df.columns = ['category','project','company','email','phone','remain_dates','achievement_rate','total_funded','total_supporters']
    print(df)
    write_csv(df)

init()
