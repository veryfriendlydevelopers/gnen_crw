import time
import os
import random
import pandas as pd
from datetime import datetime

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# UC 드라이버 옵션 설정
options = uc.ChromeOptions()
options.headless = False
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--disable-infobars')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--start-maximized')
options.page_load_strategy = 'eager'
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

# "detach" 옵션 제거
# UC에서는 detach 없이도 브라우저를 유지할 수 있음

# UC 드라이버 생성
driver = uc.Chrome(options=options)

# 로그인 페이지로 이동
driver.get("https://accounts.kakao.com/login/?continue=https%3A%2F%2Fkauth.kakao.com%2Foauth%2Fauthorize%3Fclient_id%3D36cf3898c3072e555ea6a49b299f8a06%26redirect_uri%3Dhttps%253A%252F%252Fwww.gangnamunni.com%252Fsignup%252Foauth%252Fkakao%26response_type%3Dcode%26scope%3Daccount_email%252Cbirthday%252Cname%252Cphone_number%252Ctalk_message%26through_account%3Dtrue#login")

WebDriverWait(driver, 300).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'GlobalHeader__StyledUserImage-sc-35f0e887-9'))
)

print("로그인 완료됨! 다음 단계로 진행합니다.")
# 크롤링할 페이지 URL 목록
pageList = [
    "https://www.gangnamunni.com/reviews?hospitalId=826"
]


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

            
        
        # 개선된 무한스크롤 코드
        SCROLL_PAUSE_TIME = random.uniform(2, 3)

        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            time.sleep(SCROLL_PAUSE_TIME)

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                try:
                    more_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.bg-gray-200.rounded-\[8px\].px-4.py-2.w-full"))
                    )
                    driver.execute_script("arguments[0].click();", more_button)
                    time.sleep(random.uniform(2, 3))
                    new_height = driver.execute_script("return document.body.scrollHeight")
                except:
                    print("더 이상 불러올 데이터가 없습니다.")
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