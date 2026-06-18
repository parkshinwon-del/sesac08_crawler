import requests #인터넷 요청
from bs4 import BeautifulSoup #정적 웹페이지 크롤링
from selenium import webdriver #동적 웹페이지 크롤링

import time #시간 라이브러리
from tqdm import tqdm #진행률+ for 문
import pandas as pd #클롤링한 내용을 엑셀파일로 저장하기 위해서
#xlsx->openpyxl(파이썬으로 엑셀 컨트롤)
#csv->pandas를 사용 


url = 'https://www.cheongwon.go.kr/portal/petition/open/view#'

response = requests.get(url)
#requests 라이브러리를 사용해서 웹페이지를 읽어와라(get)
print(response)

#python -m vevn'이름'으로 만들어라

#웹페이지를 분해할 bs4 객체 생성
#파싱 = 어떤 정보 덩어리에서 원하는 정보를 추출하는 것
soup = BeautifulSoup(response.text,'html.parser')
# print(response.text)

#soup 이라는 파싱객체가, 'span'이라는 양식의 class를 찾아서
#class ='category'라고 적힌 내용을 category라는 변수 이름에 저장
category = soup.find_all('span',class_ = 'category')
subject = soup.find_all('span', class_ = 'subject')
petition = soup.find_all('span', class_='text')
#print(category, subject, petition)

#크롤링한 결과물을 보기 쉬운 형태로 변환
corpus = []
for c,s,t in zip(category, subject, petition):
    corpus.append([c.text, s.text, t.text])

time.sleep(2) #2초정도 정지

df = pd.DataFrame(corpus, columns=['카테고리','제목', '청원내용'])
print(df.head())
#df.to_csv(경로)
df.to_csv('./crawling_sample.csv', index=False, encoding='utf-8-sig')
