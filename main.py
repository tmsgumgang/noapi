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
    # 실제 한국 윈도우 환경처럼 보이게 설정
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
    chrome_options.add_argument("lang=ko_KR")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        # 1. 사이트 접속 (충분히 대기)
        target_url = "https://wms.waterkorea.or.kr/wms/main/"
        driver.get(target_url)
        time.sleep(10) # 10초 대기
        driver.save_screenshot("1_initial_load.png")
        
        # 2. 기존 알림창 선제적 차단
        try:
            alert = driver.switch_to.alert
            print(f"발견된 초기 알림창 제거: {alert.text}")
            alert.accept()
        except NoAlertPresentException:
            pass

        # 3. 쿠키 주입 (기존 쿠키 삭제 후 주입)
        cookie_data = os.environ.get("MY_COOKIES")
        if cookie_data:
            driver.delete_all_cookies() # 기존 쿠키 정리
            cookies = json.loads(cookie_data)
            for cookie in cookies:
                # 보안 관련 필드 제거 및 정수화
                if 'domain' in cookie: del cookie['domain']
                if 'expiry' in cookie: cookie['expiry'] = int(cookie['expiry'])
                try:
                    driver.add_cookie(cookie)
                except:
                    pass
            print("쿠키 주입 완료")
            
            # 4. 로그인 적용 (새로고침 전후 대기)
            time.sleep(3)
            driver.refresh()
            time.sleep(10) # 로딩 대기
            
            # 5. 알림창 재발생 시 자동 끄기
            try:
                alert = driver.switch_to.alert
                print(f"새로고침 후 알림창 발생: {alert.text}")
                alert.accept()
            except NoAlertPresentException:
                pass
            
            print(f"최종 페이지 제목: {driver.title}")
            driver.save_screenshot("2_final_result.png")
        else:
            print("MY_COOKIES를 찾을 수 없습니다.")
            
    except Exception as e:
        print(f"실행 중 오류 발생: {e}")
        driver.save_screenshot("error_page.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_scraper()
