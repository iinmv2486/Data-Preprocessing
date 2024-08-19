from get_video_info import extract_video_id
from youtube_transcript_api import YouTubeTranscriptApi as yta

def get_transcipt(video_id):
    """
    비디오 id를 통해 [{'text': ... , 'start': ... , 'duration': ... }] 형태로 자막 추출
    """
    transcript = yta.get_transcript(video_id, languages=['en'])
    return transcript


def make_sentence(transcript):
    """
    추출한 자막의 text를 하나의 문장으로 가공. 
    문장은 마침표로 끝나도록 결합되며, 시작 시점은 동일하고 지속시간은 결합된 자막들의 지속시간의 합이 됨.
    """
    sentences = []
    current_sentence = ""
    current_start = None
    current_duration = 0.0

    for entry in transcript:
        text = entry['text']
        start = entry['start']
        duration = entry['duration']

        # 첫 번째 자막일 경우 시작 시간 설정
        if current_start is None:
            current_start = start

        # 문장을 현재 문장에 추가
        current_sentence += text
        current_duration += duration

        # 문장이 마침표로 끝나는지 확인
        if current_sentence.strip().endswith('.'):
            # 완성된 문장을 리스트에 추가
            sentences.append({
                'text': current_sentence.strip(),
                'start': current_start,
                'duration': current_duration
            })

            # 다음 문장을 위해 초기화
            current_sentence = ""
            current_start = None
            current_duration = 0.0

    # 마지막 문장이 마침표 없이 끝나는 경우 처리
    if current_sentence:
        sentences.append({
            'text': current_sentence.strip(),
            'start': current_start,
            'duration': current_duration
        })

    return sentences

# 예제 실행
if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=aircAruvnKk&list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi"
    # video_url = "https://www.youtube.com/watch?v=3SRh2nzN2DM&list=PL8GvYFvXM-EXSSNpkNSXUCDp_8kXa4jPF&index=16"
    video_id = extract_video_id(video_url)

    data = get_transcipt(video_id)
    processed_data = make_sentence(data)
    print(processed_data)
