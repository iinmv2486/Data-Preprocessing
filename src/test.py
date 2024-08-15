from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import re

def extract_timestamps_from_video(video_id):
    # Selenium 설정
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 브라우저 창을 열지 않음
    service = Service(executable_path='path/to/chromedriver')  # Chromedriver 경로 지정
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # YouTube 비디오 URL
    url = f"https://www.youtube.com/watch?v={video_id}"
    driver.get(url)
    
    # 페이지 로드 후 페이지 소스 가져오기
    page_source = driver.page_source
    driver.quit()
    
    # 정규식 패턴: HH:MM - Title 또는 H:MM - Title 형태의 텍스트를 추출
    pattern = r"(\d{1,2}:\d{2})\s*-\s*(.+)"
    
    # 타임스탬프와 제목을 추출
    timestamps = []
    for match in re.finditer(pattern, page_source):
        time, title = match.groups()
        timestamps.append((time, title))
    
    return timestamps

# 예제 호출
video_id = "8SF_h3xF3cE"  # 예시 비디오 ID
timestamps = extract_timestamps_from_video(video_id)
for time, title in timestamps:
    print(f"{time} - {title}")
