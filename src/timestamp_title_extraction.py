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
    previous_minutes = 0  # 이전 타임스탬프의 분을 저장

    for match in re.finditer(pattern, description):
        time_str, title = match.groups()

        # 타임스탬프가 "MM:SS" 형식인지 확인하고 필요하면 "HH:MM:SS" 형식으로 변환
        minutes, seconds = map(int, time_str.split(':'))
        if minutes < previous_minutes:
            # 이전 분보다 현재 분이 작으면 시간 단위가 변경되었음을 의미
            hours = minutes // 60
            minutes = minutes % 60
            time_str = f"{hours}:{minutes:02d}:{seconds:02d}"
        else:
            if minutes >= 60:
                hours = minutes // 60
                minutes = minutes % 60
                time_str = f"{hours}:{minutes:02d}:{seconds:02d}"
            else:
                time_str = f"{minutes:02d}:{seconds:02d}"

        previous_minutes = minutes
        timestamps.append((time_str, title))
    
    return timestamps

# API 키를 .env 파일에서 불러오기
api_key = os.getenv("YOUTUBE_API_KEY")  # .env 파일에 저장된 키를 불러옴
video_id = "8SF_h3xF3cE"  # 예시 비디오 ID
timestamps = extract_timestamps_from_description(video_id, api_key)
for time, title in timestamps:
    print(f"{time} - {title}")
