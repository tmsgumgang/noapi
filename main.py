import os
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException

def run_scraper():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    # 실제 브라우저처럼 보이기 위한 필수 설정
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        # 1. 사이트 접속
        target_url = "https://wms.waterkorea.or.kr/wms/main/"
        driver.get(target_url)
        time.sleep(3)
        
        # 2. 쿠키 주입 전 기존 알림창이 있다면 제거
        try:
            alert = driver.switch_to.alert
            print(f"초기 알림창 제거: {alert.text}")
            alert.accept()
        except NoAlertPresentException:
            pass

        # 3. 쿠키 주입
        cookie_data = os.environ.get("MY_COOKIES")
        if cookie_data:
            cookies = json.loads(cookie_data)
            for cookie in cookies:
                # 불필요한 속성 제거로 호환성 높임
                if 'domain' in cookie: del cookie['domain']
                if 'expiry' in cookie: cookie['expiry'] = int(cookie['expiry'])
                driver.add_cookie(cookie)
            print("쿠키 주입 성공!")
            
            # 4. 로그인 적용을 위한 새로고침 및 알림창 예외 처리
            try:
                driver.refresh()
                time.sleep(5)
            except UnexpectedAlertPresentException:
                alert = driver.switch_to.alert
                print(f"새로고침 중 알림창 발생: {alert.text}")
                alert.accept() # 확인 버튼 강제 클릭
            
            print(f"최종 페이지 제목: {driver.title}")
            driver.save_screenshot("final_check.png")
        else:
            print("쿠키를 찾을 수 없습니다.")
            
    except Exception as e:
        print(f"실행 중 오류 발생: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_scraper()
