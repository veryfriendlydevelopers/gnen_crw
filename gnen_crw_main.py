import time
import os
import csv
import random
import pandas as pd
import numpy as np
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

# # 아이디, 비밀번호 가져오기
# with open('id.txt', 'r', encoding='utf-8') as f:
#     login_id = f.read().strip()
# with open('password.txt', 'r', encoding='utf-8') as file:
#     login_pw = file.read().strip()

# 크롬 옵션 설정
chrome_options = Options()
chrome_options.headless = False
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_argument('--disable-infobars')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--start-maximized')
chrome_options.page_load_strategy = 'eager'
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)
chrome_options.add_experimental_option("detach", True)

# 드라이버 생성
driver = webdriver.Chrome(options=chrome_options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

# 크롤링할 페이지 URL 목록
pageList = [
    "https://www.gangnamunni.com/reviews?hospitalId=826"
]



# 로그인 프로세스스

# # 로그인 페이지 접속
# driver.get("https://accounts.kakao.com/login/?continue=https%3A%2F%2Fkauth.kakao.com%2Foauth%2Fauthorize%3Fclient_id%3D36cf3898c3072e555ea6a49b299f8a06%26redirect_uri%3Dhttps%253A%252F%252Fwww.gangnamunni.com%252Fsignup%252Foauth%252Fkakao%26response_type%3Dcode%26scope%3Daccount_email%252Cbirthday%252Cname%252Cphone_number%252Ctalk_message%26through_account%3Dtrue#login")
# WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.ID, 'loginId--1'))
# ).send_keys(login_id)

# time.sleep(random.uniform(0.5, 1))

# WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.ID, 'password--2'))
# ).send_keys(login_pw)

# # 로그인 버튼 클릭
# WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn_g.highlight.submit'))
# ).click()

# time.sleep(3)

# 브라우저 실행
driver = webdriver.Chrome()

# 로그인 페이지로 이동
driver.get("https://accounts.kakao.com/login/?continue=https%3A%2F%2Fkauth.kakao.com%2Foauth%2Fauthorize%3Fclient_id%3D36cf3898c3072e555ea6a49b299f8a06%26redirect_uri%3Dhttps%253A%252F%252Fwww.gangnamunni.com%252Fsignup%252Foauth%252Fkakao%26response_type%3Dcode%26scope%3Daccount_email%252Cbirthday%252Cname%252Cphone_number%252Ctalk_message%26through_account%3Dtrue#login")

# 수동 로그인을 위해 기다림 (예: 로그인 후 보이는 특정 요소 기다림)
element = WebDriverWait(driver, 300).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'GlobalHeader__StyledUserImage-sc-35f0e887-9'))
)

print("로그인 완료됨! 다음 단계로 진행합니다.")




# # 변수들 담아올 리스트

# gn_hname = [] # 병원이름
# gn_names = [] # 작성자
# gn_dates = [] # 작성날짜
# gn_reviews= [] # 리뷰본문



# for page in pageList:
#     try:
#         driver.get(page)

#         # 페이지 로딩 기다림
#         WebDriverWait(driver, 20).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, "h3.UserProfile__StyledName-sc-36315857-4"))
#         )

#         time.sleep(random.uniform(1.5, 2.5))

#         # 더보기 버튼 클릭 (존재하면 한번 클릭)
#         try:
#             more_button = WebDriverWait(driver, 5).until(
#                 EC.element_to_be_clickable(
#                     (By.CSS_SELECTOR, "button.bg-gray-200.rounded-\[8px\].px-4.py-2.w-full"))
#             )
#             driver.execute_script("arguments[0].click();", more_button)
#             time.sleep(random.uniform(2, 3))
#         except Exception as e:
#             print("더보기 버튼 없음 또는 클릭 실패:", e)

#         # 더보기 이후 무제한 스크롤 내리기 (페이지 끝까지)
#         last_height = driver.execute_script("return document.body.scrollHeight")

#         while True:
#             driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#             time.sleep(random.uniform(2, 3))  # 페이지 로딩 시간 기다림
            
#             new_height = driver.execute_script("return document.body.scrollHeight")
#             if new_height == last_height:  # 더 이상 내려가지 않으면 중지
#                 break
#             last_height = new_height

#         # 여기서 부터 데이터 수집
        
        
        
#         #작성자 수집
#         namesList = driver.find_elements(By.CSS_SELECTOR, "h3.UserProfile__StyledName-sc-36315857-4")
#         for name_el in namesList:
#             full_text = name_el.text.strip()
#             r_name = full_text.split('Lv.')[0].strip()
#             if r_name:
#                 gn_names.append(r_name)
                
#         #날짜 수집
#         datesList = driver.find_elements(By.CSS_SELECTOR, "span.new__StyledDate-sc-1ee6cb43-4.ggzbIA")
#         for date_el in datesList:
#             r_date = date_el.text.strip().split()[0]  # 공백으로 나눈 뒤 날짜만 추출
#             if r_date:
#                 gn_dates.append(r_date)
                
                
#         #본문 수집
#         reviewsList = driver.find_elements(By.CSS_SELECTOR, "p.new__StyledDescription-sc-1ee6cb43-10.kRHXmV")

#         for review_el in reviewsList:
#             r_review = review_el.text.strip()
#             if r_review:
#                 gn_reviews.append(r_review)

#         # 중간 결과 확인 (진행 상황 파악 가능)
#         print(f"현재 페이지에서 수집된 리뷰 개수: {len(namesList)}")

#         # 페이지간 휴식
#         time.sleep(random.uniform(2, 4))

#     except Exception as e:
#         print(f"오류 발생: {e}")
#         time.sleep(5)
        
        
#     #병원 이름(리뷰 수 만큼 병원 이름을 리스트에 반복해서 넣음음)
#         hname = driver.find_element(By.CSS_SELECTOR, "h1.sc-kyMESl bxvimI")
#         for i in range(len(namesList)):
#             gn_hname.append(hname)
            
            
#     #데이터프레임 생성
#     df = pd.DataFrame()
#     df['Hospital_Name'] = gn_hname
#     df['Names'] = gn_names
#     df['Dates'] = gn_dates
#     df['Reviews'] = gn_reviews

#     # output 폴더가 없으면 생성
#     os.makedirs('output', exist_ok=True)
#     now = datetime.now().strftime("%Y%m%d_%H%M%S")
#     filename = f"{hname}_{now}.csv"

#     # 데이터프레임 저장
#     df.to_csv(f'output/{filename}', index=False, encoding='utf-8-sig')
#     print(f"{hname} 수집 완료!")
    
    
    
# print("작업끝!")



gn_hname = [] # 병원이름
gn_names = [] # 작성자
gn_dates = [] # 작성날짜
gn_reviews= [] # 리뷰본문

for page in pageList:
    try:
        driver.get(page)

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h3.UserProfile__StyledName-sc-36315857-4"))
        )

        time.sleep(random.uniform(1.5, 2.5))

        # 더보기 버튼 클릭
        try:
            more_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.bg-gray-200.rounded-\[8px\].px-4.py-2.w-full"))
            )
            driver.execute_script("arguments[0].click();", more_button)
            time.sleep(random.uniform(2, 3))
        except:
            pass

        # # 무제한 스크롤
        # last_height = driver.execute_script("return document.body.scrollHeight")
        # while True:
        #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #     time.sleep(random.uniform(2, 3))
        #     new_height = driver.execute_script("return document.body.scrollHeight")
        #     if new_height == last_height:
        #         break
        #     last_height = new_height
            
        # # 스크롤 횟수 제한한
        # for _ in range(1, 249):
        #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #     time.sleep(random.uniform(2, 3))
            
            
        #개선된 스크롤?
        last_height = driver.execute_script("return document.body.scrollHeight")
        scroll_position = 0
        increment = 1000  # 픽셀 단위 조정 가능

        while scroll_position < last_height:
            scroll_position += increment
            driver.execute_script(f"window.scrollTo(0, {scroll_position});")
            time.sleep(random.uniform(1, 2))

            new_height = driver.execute_script("return document.body.scrollHeight")
            if scroll_position >= new_height:
                break
            last_height = new_height


        # 병원 이름 수집
        hname = driver.find_element(By.CSS_SELECTOR, "h1.sc-kyMESl.bxvimI").text.strip()

        # 리뷰 단위로 통합하여 데이터 수집
        review_elements = driver.find_elements(By.CSS_SELECTOR, "div.new__StyledReviewCard-sc-1ee6cb43-1.fanWCp") # 리뷰 개별 카드의 최상단 요소로 선택
        for review in review_elements:
            # 작성자
            try:
                name = review.find_element(By.CSS_SELECTOR, "h3.UserProfile__StyledName-sc-36315857-4.AYCqw").text.strip().split('Lv.')[0].strip()
            except:
                name = ""

            # 날짜
            try:
                date = review.find_element(By.CSS_SELECTOR, "span.new__StyledDate-sc-1ee6cb43-4.ggzbIA").text.strip().split()[0]
            except:
                date = ""

            # 본문
            try:
                content = review.find_element(By.CSS_SELECTOR, "p.new__StyledDescription-sc-1ee6cb43-10.kRHXmV").text.strip()
            except:
                content = ""

            # 리스트에 추가 (값이 비어있어도 추가하여 길이를 동일하게 유지)
            gn_hname.append(hname)
            gn_names.append(name)
            gn_dates.append(date)
            gn_reviews.append(content)

        # 중간 확인
        print(f"{hname} 페이지에서 수집된 리뷰 개수: {len(review_elements)}")

        time.sleep(random.uniform(2, 4))

        # 데이터프레임 생성 및 저장
        df = pd.DataFrame({
            'Hospital_Name': gn_hname,
            'Names': gn_names,
            'Dates': gn_dates,
            'Reviews': gn_reviews
        })

        os.makedirs('output', exist_ok=True)
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{hname}_{now}.csv"
        df.to_csv(f'output/{filename}', index=False, encoding='utf-8-sig')

        print(f"{hname} 수집 완료!")

        # 각 병원별로 리스트 초기화(중요)
        gn_hname.clear()
        gn_names.clear()
        gn_dates.clear()
        gn_reviews.clear()

    except Exception as e:
        print(f"오류 발생: {e}")
        time.sleep(5)

print("작업 끝!")