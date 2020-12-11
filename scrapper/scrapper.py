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

def get_infos(url):
    print('scrapping...',url)
    row = []
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')
    if soup.find('div', {'class': 'notPermittedPage'}) != None:
        return 
    else :
        maker_info = soup.find('div', {'id': 'reward-maker-info'})
        title_info = soup.find('h2', {'class': 'title'}).find('a')
        subject_info = soup.find('p', {'class': 'title-info'})
        project_info = soup.find('div', {'class': 'project-state-info'}).find('div', {'class': 'state-box'})

        company = maker_info['data-maker-name']
        email = maker_info['data-host-email']
        phone = maker_info['data-host-call-num']
        project = title_info.get_text(strip=True)
        subject = subject_info.get_text(strip=True)
        if project_info.find('p', {'class': 'remaining-day'}) != None:
            project_status = project_info.find('p', {'class': 'remaining-day'}).get_text(strip=True)
        else:
            project_status = 'test'
        project_achievement_rate = project_info.find('p', {'class': 'achievement-rate'}).find('strong').get_text(strip=True) + '%'
        project_total_amount = project_info.find('p', {'class': 'total-amount'}).find('strong').get_text(strip=True)
        project_total_supporter = project_info.find('p', {'class': 'total-supporter'}).find('strong').get_text(strip=True)

        row.extend((
            subject,
            project,
            company,
            email,
            phone,
            project_status,
            project_achievement_rate,
            project_total_amount,
            project_total_supporter
        ))
        return row

def get_campaign_paths(driver):
    paths = []
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')
    test = soup.select('div.ProjectCardList_item__1owJa')
    for v in range(len(test)):
        link = test[v].find('a')['href']
        paths.append(link)

    return paths

def write_csv(df):
    df.to_csv(Path('/Users/maketing/Desktop','wadiz_pet_db.csv'))

def init():
    raw_data = []
    driver = webdriver.Chrome('/Users/maketing/Downloads/chromedriver')
    driver.implicitly_wait(3) 
    driver.get('https://www.wadiz.kr/web/wreward/category/297?keyword=&endYn=ALL&order=recommend')

    scroll_downer(driver)
    paths = get_campaign_paths(driver)
    for v in paths:
        url = 'https://www.wadiz.kr' + v
        row = get_infos(url)
        if row != None:
            raw_data.append(row)
        else:
            continue

    df = pd.DataFrame(raw_data)
    df.columns = ['category','project','company','email','phone','remain_dates','achievement_rate','total_funded','total_supporters']
    print(df)
    write_csv(df)

init()
# for n in test:
#     print(n.text.strip())
# def get_last_page(URL):
#     result = requests.get(URL)
#     soup = BeautifulSoup(result.text, 'html.parser')
#     #get pagination(div 중 페이지)
#     pages = soup.find('div', {'class': 's-pagination'}).find_all('a')
#     last_page = pages[-2].get_text(strip=True)
#     return int(last_page)


# def extract_job(html):
#     job_id = html['data-jobid']
#     print(job_id)
#     title = html.find('div', {'class': 'grid--cell fl1'}).find('a')['title']
#     company, location = html.find('h3', {
#         'class': 'fc-black-700 fs-body1 mb4'
#     }).find_all(
#         'span', recursive=False)
#     company = company.get_text(strip=True).strip(' \r')
#     location = location.get_text(strip=True)

#     return {
#         'title': title,
#         'company': company,
#         'location': location,
#         'link': f'https://stackoverflow.com/jobs/{job_id}'
#     }


# # def extract_jobs(last_page, URL):
#     jobs = []
#     for page in range(last_page):
#         print(f'Scrapping SO : Page : {page}')
#         result = requests.get(f'{URL}{page+1}')
#         soup = BeautifulSoup(result.text, 'html.parser')
#         results = soup.find_all('div', {'class': '-job'})
#         print(results)
#         for result in results:
#             # print(result['data-jobid'])
#             job = extract_job(result)
#             jobs.append(job)
#         return jobs


# def get_jobs():
#     URL = f'https://www.wadiz.kr/web/wreward/category/287?keyword=&endYn=ALL&order=recommend'
#     page = get_last_page(URL)
#     # jobs = extract_jobs(page, URL)
    
#     # return jobs
# get_jobs()