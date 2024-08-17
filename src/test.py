import os
from googleapiclient.discovery import build
import re
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

def extract_timestamps_from_description(video_id, api_key):
    # YouTube Data API 클라이언트 생성
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    # 비디오 정보 요청
    request = youtube.videos().list(
        part="snippet",
        id=video_id
    )
    response = request.execute()
    
    # 비디오 설명 추출
    description = response['items'][0]['snippet']['description']
    
    # 정규식 패턴: HH:MM - Title 또는 H:MM - Title 형태의 텍스트를 추출
    pattern = r"(\d{1,2}:\d{2})\s*-\s*(.+)"
    
    # 타임스탬프와 제목을 추출
    timestamps = []
    for match in re.finditer(pattern, description):
        time, title = match.groups()
        timestamps.append((time, title))
    
    return timestamps

# API 키를 .env 파일에서 불러오기
api_key = os.getenv("YOUTUBE_API_KEY")  # .env 파일에 저장된 키를 불러옴
video_id = "8SF_h3xF3cE"  # 예시 비디오 ID
timestamps = extract_timestamps_from_description(video_id, api_key)
for time, title in timestamps:
    print(f"{time} - {title}")
