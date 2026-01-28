import os
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def run_scraper():
    chrome_options = Options()
    chrome_options.add_argument("--headless") # 화면 없이 실행
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # 1. 사이트 기본 접속
    target_url = "여기에_측정망_주소를_넣으세요"
    driver.get(target_url)
    time.sleep(2)

    # 2. 쿠키 주입
    try:
        cookies = json.loads(os.environ.get("MY_COOKIES"))
        for cookie in cookies:
            driver.add_cookie(cookie)
        print("쿠키 주입 성공!")

        # 3. 로그인 후 화면으로 이동 확인
        driver.refresh()
        time.sleep(3)
        print(f"현재 페이지 제목: {driver.title}")

    except Exception as e:
        print(f"오류 발생: {e}")

    driver.quit()

if __name__ == "__main__":
    run_scraper()
