#helper modules
from helpers.listen import listen
from helpers.say import say

from youtubesearchpython import VideosSearch
import webbrowser

def youtube_video(query):
    query = query.replace("jarvis play", "").strip()
    query = query.replace(" ", "+")
    search_query = query
    videos_search = VideosSearch(search_query, limit=1)
    results = videos_search.result()
    
    if results['result']:
        first_video_url = results['result'][0]['link']
        chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s" 
        webbrowser.get(chrome_path).open(first_video_url, new=2)
    else:
        say("No search results found")