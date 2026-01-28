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
    chrome_options.add_argument("--window-size=1920,1080")
    # 실제 브라우저처럼 보이게 하기 위한 에이전트 설정
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        # 1. 전달해주신 새 주소로 접속
        target_url = "https://wms.waterkorea.or.kr/wms/main/" 
        driver.get(target_url)
        time.sleep(3)
        print(f"사이트 접속 성공: {driver.title}")
        
        # 2. 쿠키 주입
        cookie_data = os.environ.get("MY_COOKIES")
        if cookie_data:
            cookies = json.loads(cookie_data)
            for cookie in cookies:
                # 쿠키 도메인 설정이 현재 주소와 맞지 않을 경우를 대비해 도메인 속성 제거
                if 'domain' in cookie:
                    del cookie['domain']
                if 'expiry' in cookie:
                    cookie['expiry'] = int(cookie['expiry'])
                driver.add_cookie(cookie)
            print("쿠키 주입 성공!")
            
            # 3. 로그인 상태 적용을 위한 새로고침
            driver.refresh()
            time.sleep(5)
            print(f"로그인 후 확인된 페이지 제목: {driver.title}")
            
            # 디버깅용 스크린샷 (로그가 성공하더라도 화면을 확인하기 위함)
            driver.save_screenshot("check_login.png")
        else:
            print("쿠키 데이터(MY_COOKIES)를 찾을 수 없습니다.")
            
    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_scraper()
