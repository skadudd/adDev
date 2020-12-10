import requests
from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.Chrome('/Users/beomi/Downloads/chromedriver')
driver.get('https://www.wadiz.kr/web/wreward/category/287?keyword=&endYn=ALL&order=recommend')

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


# def extract_jobs(last_page, URL):
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