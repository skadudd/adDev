import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from pathlib import Path
import pandas as pd


def scroll_downer(driver):
    last_height = 0
    SCROLL_PAUSE_TIME = 3
 
    while True:
        # 화면 최하단으로 스크롤 다운
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
        # 페이지 로드를 기다림
        time.sleep(SCROLL_PAUSE_TIME)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight-50);")
        time.sleep(SCROLL_PAUSE_TIME)
    
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
    
        # 새로운 높이가 이전 높이와 변하지 않았을 경우 스크롤 종료
        if new_height == last_height:
            break
        
        # 스크롤 다운이 된다면 스크롤 다운이 된 후의 창 높이를 새로운 높이로 갱신
        last_height = new_height

def get_infos(url,driver):
    print('scrapping...',url)
    html = driver.page_source
    print(html)
    soup = BeautifulSoup(html,'html.parser')
    test = soup.select('div.MuiPaper-root MuiTableContainer-root MuiPaper-elevation1 MuiPaper-rounded')
    print(test)

def access_token(url_login,driver):
    driver.get(url_login)
    driver.find_element_by_xpath('//*[@id="root"]/div/main/div[2]/form/div/div/input').send_keys('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwczovL2hhc3VyYS5pby9qd3QvY2xhaW1zIjp7IngtaGFzdXJhLWFsbG93ZWQtcm9sZXMiOlsiY3JtIl0sIngtaGFzdXJhLWRlZmF1bHQtcm9sZSI6ImNybSJ9LCJpYXQiOjE2MDc2Njg0MDksImlzcyI6ImNyZWF0YWJsZS1zY3JpcHQtam9obndvb2sifQ.48UO-qxGNjh28BerWdoPrZHfidxIGUne2_qUIeuD1M0')
    driver.implicitly_wait(3)
    driver.find_element_by_xpath('//*[@id="root"]/div/main/div[2]/form/button').click()
    driver.find_element_by_xpath('//*[@id="root"]/div/header/div/button/span[1]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="root"]/div/div/div/ul/div[3]').click()
    time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')
    # print(soup.prettify())
    test = soup.select('div.MuiPaper-root MuiTableContainer-root MuiPaper-elevation1 MuiPaper-rounded')
    print(test)

def init():
    url_login = 'https://bo.capa.ai/login'
    url = 'https://bo.capa.ai/client'
    driver = webdriver.Chrome('/Users/kim/Downloads/chromedriver')
    driver.implicitly_wait(1)
    access_token(url_login,driver)

    # scroll_downer(driver)
    # get_infos(url,driver)

init()