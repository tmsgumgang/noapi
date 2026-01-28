import os
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def run_scraper():
    # 1. 크롬 브라우저 옵션 설정 (GitHub Actions 환경용)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 화면 없이 실행 (필수)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    # 실제 사람처럼 보이게 하기 위한 User-Agent 설정
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    # 2. 드라이버 실행
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        # 3. 국가수질자동측정망 메인 페이지 접속
        # 보안상 실제 도메인 주소로 변경하여 사용하세요.
        target_url = "https://tms.water.or.kr/" 
        driver.get(target_url)
        time.sleep(3) # 페이지 로딩 대기
        print(f"초기 접속 완료: {driver.title}")

        # 4. GitHub Secrets에서 쿠키 불러오기 및 주입
        cookie_json = os.environ.get("MY_COOKIES")
        if not cookie_json:
            print("오류: MY_COOKIES 환경 변수가 설정되지 않았습니다.")
            return

        cookies = json.loads(cookie_json)
        for cookie in cookies:
            # 쿠키의 expiry(만료일) 값이 소수점일 경우 에러가 날 수 있어 정수 처리
            if 'expiry' in cookie:
                cookie['expiry'] = int(cookie['expiry'])
            driver.add_cookie(cookie)
        
        print("쿠키 주입 완료!")

        # 5. 쿠키 주입 후 페이지 새로고침 (로그인 상태 확인)
        driver.refresh()
        time.sleep(5)
        
        # 6. 결과 확인: 로그인 후 나타나는 특정 요소나 페이지 제목 출력
        print(f"로그인 후 페이지 제목: {driver.title}")
        
        # 스크린샷 저장 (디버깅용 - GitHub Actions의 Artifact에서 확인 가능)
        driver.save_screenshot("after_login.png")
        print("스크린샷 저장 완료: after_login.png")

        # [실제 데이터 추출 로직 예시 - 나중에 사이트 구조에 맞춰 수정 필요]
        # data = driver.find_element(By.ID, "some_id").text
        # print(f"추출된 데이터: {data}")

    except Exception as e:
        print(f"실행 중 오류 발생: {str(e)}")
    
    finally:
        driver.quit()
        print("브라우저를 종료합니다.")

if __name__ == "__main__":
    run_scraper()
