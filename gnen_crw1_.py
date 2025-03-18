import time
import csv
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

# 아이디, 비밀번호 가져오기
with open('id.txt', 'r', encoding='utf-8') as f:
    login_id = f.read().strip()
with open('password.txt', 'r', encoding='utf-8') as file:
    login_pw = file.read().strip()

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
    "https://www.gangnamunni.com/reviews?hospitalId=322",
    "https://www.gangnamunni.com/reviews?hospitalId=826"
]

gn_names = []

# 로그인 페이지 접속
driver.get("https://accounts.kakao.com/login/?continue=https%3A%2F%2Fkauth.kakao.com%2Foauth%2Fauthorize%3Fclient_id%3D36cf3898c3072e555ea6a49b299f8a06%26redirect_uri%3Dhttps%253A%252F%252Fwww.gangnamunni.com%252Fsignup%252Foauth%252Fkakao%26response_type%3Dcode%26scope%3Daccount_email%252Cbirthday%252Cname%252Cphone_number%252Ctalk_message%26through_account%3Dtrue#login")
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, 'loginId--1'))
).send_keys(login_id)

time.sleep(random.uniform(0.5, 1))

WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, 'password--2'))
).send_keys(login_pw)

# 로그인 버튼 클릭
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn_g.highlight.submit'))
).click()

time.sleep(3)





# # 페이지 별 이름 수집
# for page in pageList:
#     try:
#         driver.get(page)
        
#         WebDriverWait(driver, 20).until(
#             EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h3.UserProfile__StyledName-sc-36315857-4"))
#         )
        
#         time.sleep(random.uniform(2, 4))
        
        
        
#         # 이름 추출 (span 제외)
#         namesList = driver.find_elements(By.CSS_SELECTOR, "h3.UserProfile__StyledName-sc-36315857-4")
#         for name_el in namesList:
#             full_text = name_el.text.strip()
#             r_name = full_text.split('Lv.')[0].strip()
#             if r_name:
#                 gn_names.append(r_name)
                
#         # 서버 부하 방지를 위한 대기
#         time.sleep(random.uniform(1.5, 3.5))
        
#     except Exception as e:
#         print(f"오류 발생: {e}")
#         time.sleep(5)

# # 최종 결과 출력 (확인용)
# print(gn_names)





















# gn_names = []

# for page in pageList:
#     try:
#         driver.get(page)

#         # 페이지 로딩 기다림
#         WebDriverWait(driver, 20).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, "h3.UserProfile__StyledName-sc-36315857-4"))
#         )

#         # 초기에 페이지를 최대한 아래로 스크롤 (최대 10번 반복)
#         last_height = driver.execute_script("return document.body.scrollHeight")
#         for _ in range(10):
#             driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#             time.sleep(random.uniform(1.5, 2.5))
#             new_height = driver.execute_script("return document.body.scrollHeight")
#             if new_height == last_height:
#                 break
#             last_height = new_height

#         # "더보기" 버튼 클릭 (있으면 클릭)
#         try:
#             more_button = WebDriverWait(driver, 5).until(
#                 EC.element_to_be_clickable(
#                     (By.CSS_SELECTOR, "button.bg-gray-200.rounded-\[8px\].px-4.py-2.w-full"))
#             )
#             driver.execute_script("arguments[0].click();", more_button)
#             time.sleep(random.uniform(2, 3))
#         except Exception as e:
#             print("더보기 버튼이 없습니다:", e)

#         # 더보기 버튼 클릭 후 다시 최대한 아래로 스크롤
#         last_height = driver.execute_script("return document.body.scrollHeight")
#         for _ in range(15):  # 더 많은 로딩을 위해 반복 횟수 증가 가능
#             driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#             time.sleep(random.uniform(1.5, 2.5))
#             new_height = driver.execute_script("return document.body.scrollHeight")
#             if new_height == last_height:
#                 break
#             last_height = new_height

#         # 모든 데이터 로딩 후 이름 수집
#         namesList = driver.find_elements(By.CSS_SELECTOR, "h3.UserProfile__StyledName-sc-36315857-4")
#         for name_el in namesList:
#             full_text = name_el.text.strip()
#             r_name = full_text.split('Lv.')[0].strip()
#             if r_name:
#                 gn_names.append(r_name)

#         # 페이지간 휴식
#         time.sleep(random.uniform(2, 4))

#     except Exception as e:
#         print(f"오류 발생: {e}")
#         time.sleep(5)

# # 최종 결과 출력
# print(gn_names, len(gn_names))








gn_names = []

for page in pageList:
    try:
        driver.get(page)

        # 페이지 로딩 기다림
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h3.UserProfile__StyledName-sc-36315857-4"))
        )

        time.sleep(random.uniform(1.5, 2.5))

        # 더보기 버튼 클릭 (존재하면 한번 클릭)
        try:
            more_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "button.bg-gray-200.rounded-\[8px\].px-4.py-2.w-full"))
            )
            driver.execute_script("arguments[0].click();", more_button)
            time.sleep(random.uniform(2, 3))
        except Exception as e:
            print("더보기 버튼 없음 또는 클릭 실패:", e)

        # 더보기 이후 무제한 스크롤 내리기 (페이지 끝까지)
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(2, 3))  # 페이지 로딩 시간 기다림
            
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:  # 더 이상 내려가지 않으면 중지
                break
            last_height = new_height

        # 모든 데이터 로딩 후 이름 수집
        namesList = driver.find_elements(By.CSS_SELECTOR, "h3.UserProfile__StyledName-sc-36315857-4")
        for name_el in namesList:
            full_text = name_el.text.strip()
            r_name = full_text.split('Lv.')[0].strip()
            if r_name:
                gn_names.append(r_name)

        # 중간 결과 확인 (진행 상황 파악 가능)
        print(f"현재 페이지에서 수집된 리뷰 개수: {len(namesList)}")

        # 페이지간 휴식
        time.sleep(random.uniform(2, 4))

    except Exception as e:
        print(f"오류 발생: {e}")
        time.sleep(5)

# 최종 결과 출력
print(f"총 수집된 리뷰 개수: {len(gn_names)}")