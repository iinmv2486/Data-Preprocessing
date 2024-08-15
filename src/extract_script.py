import re
from youtube_transcript_api import YouTubeTranscriptApi

def extract_video_id(url):
    # 유튜브 URL에서 비디오 ID 추출
    video_id_match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    if video_id_match:
        return video_id_match.group(1)
    else:
        raise ValueError("Invalid YouTube URL")

def get_youtube_transcript(url):
    try:
        video_id = extract_video_id(url)
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        for entry in transcript:
            print(f"{entry['start']} - {entry['text']}")
    except Exception as e:
        print(f"Error: {e}")

# 테스트용 URL
youtube_url = "https://www.youtube.com/watch?v=8SF_h3xF3cE&list=PLfYUBJiXbdtSvpQjSnJJ_PmDQB_VyT5iU"
get_youtube_transcript(youtube_url)
