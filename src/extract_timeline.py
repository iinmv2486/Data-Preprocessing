import re
from pytube import YouTube

def extract_timeline(description):
    if description is None:
        raise ValueError("The video description is empty or could not be retrieved.")
    
    # 타임라인 패턴 정규식: "00:00 - Description" 형식으로 된 라인 추출
    timeline_pattern = re.compile(r'(\d{1,2}:\d{2})\s*-\s*(.*)')
    matches = timeline_pattern.findall(description)
    
    timeline = {}
    for match in matches:
        time, title = match
        timeline[time] = title.strip()
    
    return timeline

def get_video_description(url):
    yt = YouTube(url)
    return yt.description

def extract_youtube_timeline(url):
    description = get_video_description(url)
    if description is None:
        print("No description found for the video or the description could not be retrieved.")
        return
    
    timeline = extract_timeline(description)
    
    if timeline:
        for time, title in timeline.items():
            print(f"{time} - {title}")
    else:
        print("No timeline found in the video description.")

# 테스트용 URL
youtube_url = "https://www.youtube.com/watch?v=8SF_h3xF3cE&list=PLfYUBJiXbdtSvpQjSnJJ_PmDQB_VyT5iU"
extract_youtube_timeline(youtube_url)
