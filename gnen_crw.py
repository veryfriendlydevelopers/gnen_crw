from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import csv
import os

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium_stealth import stealth

import numpy as np
import random



# 아이디 비밀번호 값 가져오기
with open('id.txt', 'r', encoding='utf-8') as file:
    login_id = file.read().strip()
    
with open('password.txt', 'r', encoding='utf-8') as file:
    login_pw = file.read().strip()


chrome_options = Options()

# 헤드리스 모드 비활성화 (필요하면 headless도 True로 설정 가능)
chrome_options.headless = False

# 옵션들 추가
chrome_options.add_argument('--disable-blink-features=AutomationControlled')  # 자동화 탐지 방지
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument('--disable-gpu')  # GPU 비활성화
chrome_options.add_argument('--no-sandbox')   # Sandbox 비활성화(안정성 증가)
chrome_options.add_argument('--disable-dev-shm-usage') # 리소스 문제 방지
chrome_options.add_argument('--disable-infobars') # 크롬 자동화 메시지 숨김
chrome_options.add_argument('--start-maximized') # 최대 화면 모드
chrome_options.page_load_strategy = 'eager'  # 페이지 로딩시간 단축 (필요 시 사용)

# 사용자 프로필을 사용하는 방법(더욱 실제 브라우저처럼 작동)
# chrome_options.add_argument('--user-data-dir=C:\\Users\\사용자명\\AppData\\Local\\Google\\Chrome\\User Data')

# 현재 설정 중 유지할 내용들
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

chrome_options.add_experimental_option("detach", True)  # 브라우저 종료 방지

driver = webdriver.Chrome(options=chrome_options)

# 추가 권장사항
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")  # webdriver 숨기기

# 더 안정적인 암시적 대기 (권장)
driver.implicitly_wait(10)

# 크롤링할 페이지 URL 목록
pageList = [
    "https://www.gangnamunni.com/reviews?hospitalId=322",
    "https://www.gangnamunni.com/reviews?hospitalId=826"
]

# URL을 저장할 리스트
gn_names = []
gn_dates = []
gn_tags = []
gn_rewiews = []
gn_scores = []


# 로그인 프로세스

driver.get("https://accounts.kakao.com/login/?continue=https%3A%2F%2Fkauth.kakao.com%2Foauth%2Fauthorize%3Fclient_id%3D36cf3898c3072e555ea6a49b299f8a06%26redirect_uri%3Dhttps%253A%252F%252Fwww.gangnamunni.com%252Fsignup%252Foauth%252Fkakao%26response_type%3Dcode%26scope%3Daccount_email%252Cbirthday%252Cname%252Cphone_number%252Ctalk_message%26through_account%3Dtrue#login")

input_element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, 'loginId--1'))
)
input_element.click()
input_element.send_keys(login_id)

time.sleep(0.72)

input_element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, 'password--2'))
)
input_element.click()
input_element.send_keys(login_pw)

time.sleep(0.42)

login_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn_g.highlight.submit'))
)
login_button.click()

time.sleep(5)




for page in pageList:
    driver.get(page)
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "h3.UserProfile__StyledName-sc-36315857-4"))
    )
    time.sleep(3)
    
    # 이름을 가져오기
    namesList = driver.find_elements(By.CSS_SELECTOR, "h3.UserProfile__StyledName-sc-36315857-4")
    for a in namesList:
        r_name = a.get_attribute("text")
        if r_name:
            gn_names.append(r_name)
            
    
    # # 페이지의 끝까지 스크롤하여 컨텐츠 로드
    # last_height = driver.execute_script("return document.body.scrollHeight")
    # while True:
    #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #     time.sleep(2)
    #     new_height = driver.execute_script("return document.body.scrollHeight")
        
    #     # 요소를 가져오기 (매번 드래그마다 값이 바뀌기 때문에 매번 저장)
    #     aList = driver.find_elements(By.CLASS_NAME, "common_clearfix__M6urU")
    #     for a in aList:
    #         url = a.get_attribute("href")
    #         if url:
    #             url_list.append(url)
    #             print(url)
        
        
        
        # if new_height == last_height:
        #     break
        # last_height = new_height

time.sleep(3)

# #중복되는 주소가 있을 수 있기 때문에, 중복된 값을 날려줌줌
# url_list = list(set(url_list))

# # CSV 파일로 저장
# csv_filename = "urls.csv"
# with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(["url"])  # 헤더 작성
#     for url in url_list:
#         writer.writerow([url])

# print(f"총 {len(url_list)}개의 URL이 {csv_filename} 파일에 저장되었습니다.")

# driver.close()






# # CSV 파일에서 URL 불러오기
# a_list = []
# with open("urls.csv", "r", encoding="utf-8") as csvfile:
#     reader = csv.reader(csvfile)
#     next(reader)  # 헤더 건너뛰기
#     for row in reader:
#         if row:  # 빈 행이 아니면
#             a_list.append(row[0])

# # output 폴더 생성
# output_dir = "output"
# os.makedirs(output_dir, exist_ok=True)

# def getData(url):
#     options = uc.ChromeOptions()
#     # 팝업 차단 및 원격 디버깅 포트 지정
#     options.add_argument('--disable-popup-blocking')
#     options.add_argument('--remote-debugging-port=9222')

#     # WebDriver 객체 생성 (incognito 모드 활성화)
#     driver = uc.Chrome(options=options, enable_cdp_events=True, incognito=True)

#     # selenium_stealth 설정
#     stealth(driver,
#             vendor="Google Inc. ",
#             platform="Win32",
#             webgl_vendor="intel Inc. ",
#             renderer="Intel Iris OpenGL Engine",
#             fix_hairline=True)

#     driver.implicitly_wait(2)
#     driver.execute_script(
#         "Object.defineProperty(navigator, 'plugins', {get: function() {return [1, 2, 3, 4, 5];},});"
#     )
#     driver.get(url)
#     driver.implicitly_wait(2)

#     # content-text 클래스를 가진 요소들을 찾아 텍스트 수집
#     contentList = driver.find_elements(By.CLASS_NAME, "content-text")
#     page_text = ""
#     for b in contentList:
#         page_text += b.get_attribute("innerHTML") + "\n"

#     # URL의 마지막 부분을 파일명으로 사용 (예: "3011389.txt")
#     basename = url.rstrip("/").split("/")[-1]
#     file_path = os.path.join(output_dir, f"{basename}.txt")
#     with open(file_path, "w", encoding="utf-8") as f:
#         f.write(page_text)
#     print(f"Saved file: {file_path}")

#     time.sleep(5)
#     driver.close()

# # 각 URL을 순회하며, /hotel/ URL을 /reviews/domestic/ 형식으로 변환 후 데이터 수집
# for a in a_list:
#     review_url = a.replace("/hotel/", "/reviews/domestic/")
#     print(f"변환 전 URL: {a}")
#     print(f"변환 후 URL: {review_url}")
    
#     getData(review_url)
#     time.sleep(5)
