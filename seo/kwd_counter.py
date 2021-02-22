import requests
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize

result = []

stopwords_list = open('stopwords.csv')
stopwords_list = stopwords_list.read()

text = open('/Users/maketing/content_growth_creatable/test_files/ncr_seo_ing.md','r')
content = text.read().split()

for w in content :
    if w not in stopwords_list :
        result.append(w)

word_list = pd.Series(result)
result_list = word_list.value_counts().head(10000)

print(content)