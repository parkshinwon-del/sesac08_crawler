from bs4 import BeautifulSoup #정적인 클롤링을 하겠구나~
import requests #인터넷 내용을 크롤링 하겠구나~
import pandas as pd #데이터프레임으로 내용 정리를 하겠구나~
import re #정규표현식
from html import unescape #html 형식의 깨진 글자를 복원

def clean_text(text):
    #text를 넣어서 clean_text를 실행했는데, text가 none이라면?
    if not text:
        return " "
    
    #text가 있다면(빈 값이 아니라면) 정제
    text = unescape(text.text)

    #re(정규표현식) : 텍스트를 특정한 패턴으로 찾아서, 변형
    #re.sub(패턴, 바꿀 문자, 문장) -> 문장에서 '패턴'을 찾아서 '바꿀문자'로 변형
    #a-zA-Z: 영문자 전체 ㄱ-ㅎ가-힣 :한글전체
    # \s (공백) \s+(한 칸 이상의 모든 공백)
    # r이있어야 정규표현식이 가능함

    text = re.sub(r'\s+', '', text)
    return text.strip()


def clean_text(value):
    if not value:
        return ""
    

def crawling_data(search_word):

    #1.'주소'를 정함(가져올 정보가 있는 인터넷 주소)
    #2. requests.get(주소) -> '주소'에 있는 html 을 받아옴
    # **** html->인터넷에서 정보를 표현하는 파일 형식
    #3. bs4->받아온 html을 '파싱(parsing)', 필요정보 추출
    #4. bs4.select(구분자) <div> ></div> 같은 애들
    #5. bs4.select_one(구분자)
    #6. 얻어낸 정보-> re(정규표현식)으로 '정제' or pandas로 정리 저장



    #'헤더' ->브라우저가 서버에 무언가 요청할 때, '나 이런 부라우저에요'라는 내용
    base_url = 'https://www.saramin.co.kr/zf_user/search'
    headers = {
            #요청하는 브라우저의 종류
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/126.0.0.0 Safari/537.36"
            ),
            #요청하는 언어의 종류
            "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
        }


    #리퀘스트를 보냄
    #headers : 웹페지에 정보를 요청하는 브라우저에 대한 내용
    #params : 웹페이지에 이런 정보를 요청합니다.~'검색어,검색조건'
    #timeout : 웹페이지로부터 회신이 올 때까지 기다리는 시간 최대치
    response = requests.get(base_url, headers=headers,
                            params={'searchword':search_word}, timeout=10)

    #만약 response가 <200>이라면 -> 정상
    #400에러(서버 에러, 웹페이지) /500에러 (클라이언트 에러)
    #bs4에게 html을 파싱하도록 객체 생성 beautifulSoup(html, 파서)

    soup = BeautifulSoup(response.text, 'html.parser')
    #print(response.text)
    #검색 결과 선별
    rows = []

    #find : 전통적인 선택 방식
    #select : 현대적인 선택 방식
    #soup.select(구분자) : '구분자'가 들어가는 모든 내용을 select(선택)
    #soup.find_all('div', class_='item recruit')

    for item in soup.select('div.item_recruit'):

    #1. 회사명 
        #select_one(구분자): 구분자 이름을 갖는 딱 하나만 가져와!
        corp_name = item.select_one('div.area_corp') 

    #2. 채용 정보
        job_area = item.select_one('div.area_job')

    #3. 공고 제목
        job_title = job_area.select_one('.job_tit')
        #왜 위는 아이템이 아니라 잡아레아지? ->item. 잡아레아. 이런식으로 계속 들어와야해서. 
        # 네모박스 안으로 들어가는식

        #<div>로 시작하지 않음! .job_tit/ div가 아니어도 괜찮아!
        #job_tit이라는 녀석을 찾아서 one 한개만 가져와!

    #4. 조건
        conditions = job_area.select_one('.job_condtion')
        location = ''
        condition1 = ''
        # 로케이션 콘디션원1은 초기화 즉 깨긋한 값으로 먼저 덮어씌우고 시작

        if conditions :
            span = conditions.select('span')
            #조건이 1개 이상 있다면~
            if len(span) > 0:
                #첫번째 조건은 무조건 위치이다.
                location = span[0].get_text(strip=True)

            if len(span) > 1:
                condition1 = span[1].get_text(strip=True)
        
        #5. 직무 분야
        job_sector = job_area.select_one('.job_sector')
        job_sector = (job_sector.get_text(strip=True) if job_sector else "" )

        #내가 모은 정보를 '정제' 함
        job_title = clean_text(job_title)
        location = claen_text(location)
        condition1 = clean_text(condition1)
        job_sector = clean_text(job_sector)
        corp_name = clean_text(corp_name)

        rows.append({
            '공고 이름': job_title,
            '회사 위치': location,
            '조건 1': condition1,
            '조건 2': job_sector,
            '회사 이름': corp_name

        })



    #최종적으로 얻어진 rows를 pd.DataFrame으로 감싸서 df를 만들어줌
    df= pd.DataFrame(rows)
    print(df)


#진입점(이 파이썬 파일의 '실제 실행되는 부분')
if __name__ == '__main__':
    crawling_data('인공지능')



