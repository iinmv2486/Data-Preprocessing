from youtube_transcript_api import YouTubeTranscriptApi as yta
from get_video_info import extract_video_id


def print_time(search_word, time):
    print(f"'{search_word}' was mentioned at: ")
    # calculate the accurate time according to the video's duration
    for t in time:
        hours = int(t // 3600)
        min = int((t // 60) % 60)
        sec = int(t % 60)
        print(f"{hours:02d}:{min:02d}:{sec:02d}")


def find_word(search_word, transcript):
    text = [data['text'] for data in transcript]

    time = []

    for i, line in enumerate(text):
        if search_word in line:
            start_time = transcript[i]['start']
            time.append(start_time)
       
    return time


if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=aircAruvnKk&list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi"
    video_id = extract_video_id(video_url)

    transcript = yta.get_transcript(video_id, languages=['en'])
    # output:
    """
    [
        {'text': 'This is a 3.', 'start': 4.22, 'duration': 1.18}, 
        {'text': "It's sloppily written and rendered at an extremely low resolution of 28x28 pixels, ", 'start': 6.06, 'duration': 4.709}, 
        {'text': 'but your brain has no trouble recognizing it as a 3.', 'start': 10.769, 'duration': 2.951}, 
        {'text': 'And I want you to take a moment to appreciate how ', 'start': 14.34, 'duration': 2.264},
        .
        .
        .
        {'text': "Using sigmoids didn't help training or it was very difficult ", 'start': 1091.16, 'duration': 4.39}, 
        {'text': 'to train at some point and people just tried ReLU and it happened ', 'start': 1095.55, 'duration': 4.751}, 
        {'text': 'to work very well for these incredibly deep neural networks.', 'start': 1100.301, 'duration': 4.319}, 
        {'text': 'All right thank you Lisha.', 'start': 1105.1, 'duration': 0.54}
    ]
    """
    search_word = "sigmoid"
    time = find_word(search_word, transcript)

    print_time(search_word, time)
    # output:
    """
    'sigmoid' was mentioned at: 
    00:10:32
    00:11:15
    00:11:54
    00:14:43
    00:14:50
    00:15:55
    00:17:15
    00:17:30
    00:18:11
    """

