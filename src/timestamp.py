# https://medium.com/@oladenj/extracting-timestamps-from-youtube-video-transcripts-using-python-e2329503d1e0

from youtube_transcript_api import YouTubeTranscriptApi as yta
import re

def print_time(search_word, time):
    print(f"'{search_word}' was mentioned at: ")
    # calculate the accurate time according to the video's duration
    for t in time:
        hours = int(t // 3600)
        min = int((t // 60) % 60)
        sec = int(t % 60)
        print(f"{hours:02d}:{min:02d}:{sec:02d}")


video_id = "1aA1WGON49E"
transcript = yta.get_transcript(video_id, languages=('us', 'en'))

