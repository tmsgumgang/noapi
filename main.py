import os
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def run_scraper():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # 국가수질자동측정망 접속
        driver.get("https://tms.water.or.kr/") 
        time.sleep(2)

        # 쿠키 주입
        cookie_data = os.environ.get("MY_COOKIES")
        if cookie_data:
            cookies = json.loads(cookie_data)
            for cookie in cookies:
                if 'expiry' in cookie:
                    cookie['expiry'] = int(cookie['expiry'])
                driver.add_cookie(cookie)
            print("쿠키 주입 성공!")

            driver.refresh()
            time.sleep(3)
            print(f"로그인 후 확인된 페이지 제목: {driver.title}")
        else:
            print("쿠키를 찾을 수 없습니다. Secrets 설정을 확인하세요.")

    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_scraper()
