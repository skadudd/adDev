import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from pathlib import Path
import pandas as pd


def scroll_downer(driver):
    last_height = 0
    SCROLL_PAUSE_TIME = 3
 
    while True:
        # 화면 최하단으로 스크롤 다운
        #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
        # 페이지 로드를 기다림
        time.sleep(SCROLL_PAUSE_TIME)
        # element = driver.find_element_by_link_text("crowdy-btn-01")
        element = driver.find_element_by_xpath("//font[text()='리워드 프로젝트 더보기']")
        
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

def get_infos(url,driver):
    print('scrapping...',url)
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')
    
    # project_title = 
    remaning_date = soup.select('div.reward-info-box > div.mt5')[0]
    achievement_rate = soup.select('div.reward-info-box > div.mt20 > span.reward-info-now')
    total_funded = soup.select('div.reward-info-box > div.reward-info-amount')
    total_supporters = soup.select('div.reward-info-box > div.mt5 > span.reward-info-now')[1]
    # company = soup.select('div.reward-info-box > detail_order_info mt25 xs-mt15 reward-order1-0 > span.reward-info-now').get_text(strip=True)
    # email = 
    
    print(remaning_date)
    print(achievement_rate)
    print(total_funded)
    print(total_supporters)


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
    df.to_csv(Path('/Users/maketing/Desktop','wadiz_pet_db.csv'))

def init():
    raw_data = []
    driver = webdriver.Chrome('/Users/maketing/Downloads/chromedriver')
    driver.implicitly_wait(3) 
    driver.get('https://www.ycrowdy.com/reward/list')
    scroll_downer(driver)
    paths = get_campaign_paths(driver)
    
    for v in paths:
        url = 'https://www.ycrowdy.com' + v
        row = get_infos(url,driver)
        if row != None:
            raw_data.append(row)
        else:
            continue

    # df = pd.DataFrame(raw_data)
    # df.columns = ['category','project','company','email','phone','remain_dates','achievement_rate','total_funded','total_supporters']
    # print(df)
    # write_csv(df)

init()
