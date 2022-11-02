import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import datetime

with open('C:\\Users\\ASIA-03\\workspace\\전기차_부정어.txt', encoding='utf-8') as neg:         # 부정어 파일 오픈
    negative = neg.readlines()
with open('C:\\Users\\ASIA-03\\workspace\\전기차_긍정어.txt', encoding='utf-8') as pos:         # 긍정어 파일 오픈
    positive = pos.readlines()

negative = [neg.replace('\n', '') for neg in negative]              # 오픈한 부정어 파일 리스트로 변경
positive = [pos.replace('\n', '') for pos in positive]              # 오픈한 긍정어 파일 리스트로 변경        

d = datetime.date(2018,6,5)                 # 크롤링 시작 날짜
today =  datetime.date(2019,1,1)            # 크롤링 종료 직후 날짜

date_list = []                              # 년월일 리스트
titles_list = []                            # 기사 제목 리스트
labels_list = []                            # 긍정 부정 판별 리스트


while(not d==today):                        # 지정 날짜까지 반복
    year = "{:%Y}".format(d)                # 검색포탈 링크에 입력할 연도
    month = "{:%m}".format(d)               # 검색포탈 링크에 입력할 월
    day = "{:%d}".format(d)                 # 검색포탈 링크에 입력할 일
    print(d)                                # 크롤링 중인 날짜
    for i in range(100):                    # 

        num = i *10 + 1                     # 기사 목록 페이지
        
        # 일자별 전기차 관련 지면기사 검색 링크
        url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EC%A0%84%EA%B8%B0%EC%B0%A8&sort=2&photo=3&field=0&pd=3&ds="+str(year)+'.'+str(month)+'.'+str(day)+"&de=2022.05.15&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:from"+str(year)+str(month)+str(day)+'to'+str(year)+str(month)+str(day)+",a:all&start=" + str(num)
        req = requests.get(url)                     # url 받아오기
        soup = BeautifulSoup(req.text, 'lxml')      # url 페이지 파싱
        titles_iter = soup.select("a.news_tit")     # 뉴스 제목 태그 선택
        
        for title in titles_iter:                   # 기사 제목들마다 반복처리
            title_data = title.text                 # 읽어온 기사 제목 텍스트화
            clean_title = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\|\(\)\[\]\<\>`\'…\"\"》]' , '', title_data)    # 기사에서 특수문자 제거
            negative_flag = False                                                                            # 부정태그 초기화
            label = 0                                                                                        # 긍부정 판단 태그 디폴트(중립=0)

            for i in range(len(negative)):                                                                   # 부정어 리스트로  부정어 검사 반복 실행
                if negative[i] in clean_title:                                                                  # 기사 제목이 부정어를 포함할 경우
                    label = -1                                                                                  # 긍부정 판단 태그 부정으로 설정(부정= -1)
                    negative_flag = True                                                                        # 부정 플래그 설정
                    
                    print('negative 비교단어 : ', negative[i], 'clean_title : ', clean_title)               
                    break                                                                                   # 부정 판단 반복문 탈출
            if negative_flag == False:
                for i in range(len(positive)):                                                              # 긍부정 태그가 부정이 아닐 경우(중립일 경우) 긍정어 검사 반복 실행
                    if positive[i] in clean_title:                                                           # 기사 제목이 긍정어를 포함할 경우
                        label = 1                                                                           # 긍부정 판단 태그 긍정으로 설정(긍정= -1)
                        
                        print('positive 비교단어 : ', positive[i], 'clean_title', clean_title)
                        break                                                                               # 긍정 판단 반복문 탈출
            titles_list.append(title_data)                                                                      # 처리한 기사 제목 리스트에 추가
            date_list.append(d)                                                                             # 처리한 기사 일자 리스트에 추가
            labels_list.append(label)                                                                       # 처리한 기사 긍부정 판단 리스트에 추가

    d+=datetime.timedelta(+1)                                                                             # 익일 기사 검색으로 변경

my_title_df = pd.DataFrame({'date':date_list, 'title':titles_list, 'label':labels_list})                    # 일자, 제목, 긍부정판단 으로 데이터프레임 생성
print(my_title_df)

def dftoCsv(my_title_df):                                                                                             # CSV 생성함수
    my_title_df.to_csv(('전기차여론_2018_2.csv'), sep=',', index = False, na_rep='NaN', encoding='utf-8-sig')

dftoCsv(my_title_df)                                                                                                    # CSV 파일 생성