# -*- coding: utf-8 -*-
import os
import glob
import re
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

path = '/Users/kim/'
today = date.today()
df = pd.read_csv('/Users/kim/adDev/NSA_rel_keyword/design_query.csv')
kwd = df['연관 검색어'][0]
print(df)
input_file = "../query/attr"

# def merge_csv() : 
#     #input_file = '/Users/maketing/adDev/DB_for_GA_naver/'
#     #output_file = '/Users/maketing/adDev/DB_of_naver_combined/'
#     allFile_list = glob.glob(os.path.join(input_file, '*.csv'))

#     all_data = []

#     for file in allFile_list:
#         df = pd.read_csv(file)
#         all_data.append(df)

#     data_combine = pd.concat(all_data, axis=0, ignore_index=True)
#     return data_combine
    
def regex_do(df):
    for v in range(len(df)) :
        text = df['연관 검색어'][v]
        
        # regex = re.compile(r'공무원|기사|실기|필기|교육|학원|인강|사|국비|기계직|교육원|강의|열역학|유동해석|박민재|코딩|라즈베리파이|기술사|9급|7급|빅데이터|한홍걸|군무원|해석|개론|이론|스토디|취업|특성화고|공기업|채용|한국사|평가|직업|진흥원|보험|공단|논술|은행|고졸|카드|구직자|문서관리|펌웨어|solidworks|문춘오|hypermesh|pdftodwg|1급|유체역학|프리미어|사무관|체험판|전기직NCS|alias|cad|피팅모델|세차기|과제|국책|물리치료사|간병인|캐디세상|의공기사|치기공사|상담사|기술사|경찰|기자|포토그래퍼|로드매니저|강사|주방보조|가수|회로|module|led컨트롤러|3D편집|브리스터포장|3D사출|PEEK사출|보조배터리디자인|캡스톤작품|일자리|포털|간이금형|창업|벤처|사회|신용|보증|예비|중소기업|1인|아르바이트|탑스타운|산업디자이너|알바|그리기|기판|오토모티브|현대|삼성|피할기|컨넥|에너지하베스팅|강동테크|중국|무역|사무소|공모전|아두이노|해석|3d프린트|PET|라이노|rhino|dwf|엠피티|CG|영상|인쇄|홍보|무료|다운|캐드|비서|잡지|프리랜서|패턴사|자격증|식품건조기|공사|압력용기|브랜드디자인|구인|MD|건드릴|영업|회계|비전공자|시각|대학원|디자인회사|기구설계|라벨부착기|벤딩기|라벨|로봇팔|협회|프린터|QDM|ODM|캠툴|렌더링|컨트롤|보드|키오스크|^디자인|ONESTOPSYSTEM|원스톱솔루션|원스톱서비스|챗봇|밋업|시그마|칼라조색|로링기|롤링기|개발대행|도자기|전시|솔루션|system|RP|출력물|오브젯|3D프린터구입|GIBBS|퀵캠|피쳐캠|스튜디오|핸드스캐너|종이|프린터|프린팅|위상|행사|수업|자료|펜|학과|크기|신발|파일|sla|sls|fdm|mjf|씽기버스|다운|설치|그래픽|인트로|주문|경화|박스|색채학|HP|신도|hvac|화물엘레베이터|덤프|리프트|마스크|체인|조립라인|승강기|FENCE|렌탈|콘베아|난간대|컨베어|스테커|콤베어|식품|콤베아|물류|풀리|규격|카프링|솔더|납디|conveyer|칩통|칩|제과|제빵|중고|컨베이어|회전초밥|수리|ROLLER|창고|접착|롤러|벨트|대추|포앙기|갈매기|대차|볼케스타|반도체자동화|솥|곡물세척기|떡기계|믹서기|사다리|자석|인발|탭핑기|용접기|오링조립기|디스펜서|해빙기|티뽑기|뽕따기|도면$|디자인$|구조물|사무실|건조|P&ID|한화|자동화시스템$|용접$|태양광|복사기|VMD|세무|장갑|천|키보드$|랜턴$|가습기$|메모북|할인점|쇼핑몰|도매|소매|도소매|총판|방명록|직구|옹접$|성형$|주형$|용기업체|자동화업체|다이캐스팅|HCI|PSD|센서|레이저|레벨볼|시설물|교통|모뎀|광|수위조절|장비$|설계$|체험|RTP|재난|FA|도면$|캠$|압출$|산출|내역|OLED|티이씨|테스트$|사무소|배관$|펜션|하우스|주상복합|타운|소방|공무|건조|조경|플랜트|태양광|이름$|용접사배구금구|추천|쇼핑몰|구매|매트|기구$|기기$|풀기|지압기|매트|기둥|동자|대문|쪽문|방수시트|받이|밧줄|유리|디딤석|화강암|파고라|세정|갈바|구입|판매|교체|S/W|통$|수입지|케이스|전단지|종류|화이트보드|파우치|충전기종류|바지|포트|스폰지|크기|시계')
        #regex = re.compile(r'강좌|박민제|ANSYSKOREA|UGNX|프로그래밍|인벤터|UG|건설$|세차장$|조종사|시스템$|기계$|관리$|제어$|냉동$|프로그램$|프로그렘|학$|최적화$|일반$|계산|1급|2급|3급|포토샵|일러스트|인증$|기직|카티아|기출|시뮬레이션|캐릭터$|기초$|CATIA|CFD|디엠유|오토데스크|NX|엔엑스|캡스톤|PCB|3D스캔|정보화|UGNX|국가|학교|$리사|직$|인벤터|^CAD|마캠|마스터캠|강좌|AUTODESK|지브러시|지브러쉬|랜더링|RHINO|rhino|스케치|스캐치|sketch|소프트웨어|^사|매니저|교사|기숙사|^사업|아트웍|SMT|반도체|솔더링|체결기$|너트|시스템개발|BIM|프린트|런너|제품기획|금형설계|개발외주|CAD|투자|CROP|모델링$|기체$|사출$|스타트업$|종합디자인|제도|정부|법인|3D프린트|랜더링|^국가|투자$|지원사업|지원|파트너스|리플렛|테크노파크|인터렉티브|인터랙티브|주택|검사기$|SMT|SUBRACK')
        regex = re.compile(r'!')
        #regex = re.compile(r'^!|금형$|강좌$|학원|그래픽|교육|멀티미디어|재료|MOCK|판매|3D스캔|수업|학과|임가공|모델링$|CAD$|기구설계$|렌탈$|쇼핑몰|대여|솔리드웍스|디자인$|기계설계회사|솔리드엣지|프린터제조사|스캐너|ulti|프로그램|인벤터|조형물$|체험$|시간$|학과$|라이노$|도면사|콘텐츠|가공$|mct|cnc|레이저|커팅|컷팅|밀링|선반|max|MAX|디자이너$|역설계|조감도|도면|카티아|디자인$|아두이노|영상|cg|vr|투시도|렌더|패키지|포장|박스|홍보|파일|생선|화장품케이스|설치|순금|봉투|종이|익스테리어|케이스$|상자$|중고|^케이스|클릭|스캐|전시회$|간단|RAVIT|PAKAGE|LIGHT|기구설계|레빗|래빗|비누|카티아|캐릭터|주택|설계$사형|주조|K-|세차장|창업|회로|이송장치|건조기|기술사|용기$케이스타트업|정부과제')
        # regex = re.compile(r'목업$|캠$|CAM$|GIBBS|공모전$|CG|알바|모델링$|설계$|모델러$|스케치$|상자|라이노')
        r = regex.search(text)
        if r != None:
            print(df['연관 검색어'][v])
            df = df.drop([v])

    return df

# data_combine = merge_csv()
# print(data_combine)
# regexed = regex_do(df)
data_combine2 = df.drop_duplicates(['연관 검색어'],keep='first')
print(data_combine2)
#print(len(df2))
# print(len(data_combine2))
# regexed.to_csv(Path(path, f'{today.year}_{today.month}_필터된키워드2.csv'), index=False)
data_combine2.to_csv(Path(path, f'{today.year}_{today.month}_필터된키워드2.csv'), index=False)