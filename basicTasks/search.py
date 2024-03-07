#helper modules
from helpers.listen import listen
from helpers.say import say

import webbrowser

def google_search(query):
    query = query.replace("jarvis search", "").replace("on Google", "").strip()
    search_url = f"https://www.google.com/search?q={query}"
    chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s" 
    webbrowser.get(chrome_path).open(search_url, new=2)