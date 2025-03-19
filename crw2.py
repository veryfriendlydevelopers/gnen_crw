import time
import os
import random
import pandas as pd
from datetime import datetime

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 크롬 옵션 설정
options = uc.ChromeOptions()
options.headless = False
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--disable-infobars')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--start-maximized')
options.page_load_strategy = 'eager'
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)
options.add_experimental_option("detach", True)

# uc 드라이버 생성
driver = uc.Chrome(options=options, use_subprocess=True)

# 카카오 로그인 페이지로 이동
driver.get("https://accounts.kakao.com/login/?continue=https%3A%2F%2Fkauth.kakao.com%2Foauth%2Fauthorize%3Fclient_id%3D36cf3898c3072e555ea6a49b299f8a06%26redirect_uri%3Dhttps%253A%252F%252Fwww.gangnamunni.com%252Fsignup%252Foauth%252Fkakao%26response_type%3Dcode%26scope%3Daccount_email%252Cbirthday%252Cname%252Cphone_number%252Ctalk_message%26through_account%3Dtrue#login")

# 수동 로그인 대기 (로그인 후 요소)
print("로그인을 완료해주세요.")
WebDriverWait(driver, 300).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'GlobalHeader__StyledUserImage-sc-35f0e887-9'))
)

print("로그인 완료됨! 크롤링 시작.")

pageList = [
    "https://www.gangnamunni.com/reviews?hospitalId=826"
]

for page in pageList:
    gn_hname, gn_names, gn_dates, gn_reviews = [], [], [], []

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

    # 무한 스크롤
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(2, 3))

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # 병원 이름
    hname = driver.find_element(By.CSS_SELECTOR, "h1.sc-kyMESl.bxvimI").text.strip()

    # 리뷰 단위 데이터 수집
    reviews = driver.find_elements(By.CSS_SELECTOR, "div.new__StyledReviewCard-sc-1ee6cb43-1.fanWCp")

    for review in reviews:
        try:
            name = review.find_element(By.CSS_SELECTOR, "h3.UserProfile__StyledName-sc-36315857-4").text.strip().split('Lv.')[0]
        except:
            name = ""

        try:
            date = review.find_element(By.CSS_SELECTOR, "span.new__StyledDate-sc-1ee6cb43-4").text.strip().split()[0]
        except:
            date = ""

        try:
            content = review.find_element(By.CSS_SELECTOR, "p.new__StyledDescription-sc-1ee6cb43-10").text.strip()
        except:
            content = ""

        gn_hname.append(hname)
        gn_names.append(name)
        gn_dates.append(date)
        gn_reviews.append(content)

    print(f"{hname} 수집된 리뷰: {len(reviews)}개")

    # DataFrame으로 저장
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

    print(f"{hname} 저장 완료!")

print("작업 끝!")

driver.quit()