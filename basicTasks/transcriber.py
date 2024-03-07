import youtube_dl
from youtube_transcript_api import YouTubeTranscriptApi

def download_video(link):
    ydl_opts = {'format': 'bestaudio/best',
                'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'wav','preferredquality': '192',}],
                'outtmpl': 'audio.wav'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])

def get_transcript(link):
    video_id = link.split('=')[-1]
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return transcript

def transcribe_video(link):
    download_video(link)
    transcript = get_transcript(link)
    text = '\n'.join([line['text'] for line in transcript])
    return text

video_link = "https://www.youtube.com/watch?v=VIDEO_ID"
transcription = transcribe_video(video_link)
print(transcription)
