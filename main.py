import os
import webbrowser
from youtubesearchpython import VideosSearch
import datetime
import promptFile
import pyperclip
from ML.sentiment import pred_sent

#deal with files
from deal_with_files.open_file import deal_with_query
from deal_with_files.vecDB import vectorize
from deal_with_files.performQA import ques_ans

#helper modules
from helpers.listen import listen
from helpers.say import say

#gen image
from ML import genImage

memory = ''

        
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
        
def google_search(query):
    query = query.replace("jarvis search", "").replace("on Google", "").strip()
    search_url = f"https://www.google.com/search?q={query}"
    chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s" 
    webbrowser.get(chrome_path).open(search_url, new=2)
    
def enterPrompt():
    say('Yes sir, go ahead')
    prompt = listen()
    prompt = prompt.lower()
    response = promptFile.return_answer(prompt)
    
    token = response.split()
    to_be_said = response.split('.')[0:3]
    say(to_be_said)
        
    if(len(token) > 30):
        say('Would you like to copy the rest of the answer to clipboard?')
        resp = listen().lower()
        if resp == 'yes do that':
            pyperclip.copy(response)
            say('Copied')
    
    if not os.path.exists('prompt_answers'):
        os.mkdir('prompt_answers')
    
    with open(f'prompt_answers/{prompt}', 'w') as f:
        f.write(response)

def chat():
    global memory
    count = 0
    say('What can I help you with?')
    while count != 1:
        query = listen().lower()
        if 'error' in query:
            continue
        if 'jarvis quit chatting' in query:
            count = 1
        memory += f'Sahil : {query}\n Jarvis: '
        response = promptFile.return_answer(memory)
        say(response)
        memory += f'{response}\n'
    return 'Nice talking with you sir!'

def time():
    time = datetime.datetime.now().strftime('%H:%M:%S')
    say(f'Sir, the time is {time}')
    
if __name__ == '__main__':
    print('hi')
    say('Jarvis activated')
    
    while True:
        print('Listening')
        query = listen()
        query = query.lower()
        if query:
            # sentiment = pred_sent(query)
            # if(sentiment and sentiment['label'] == 'positive' and sentiment['score'] >= 0.9):
            print(query)
            #     say("You seem to be in a happy mood sir!")
                
            if 'jarvis play' in query:
                youtube_video(query)
            elif query.startswith('jarvis search') and query.endswith('on google'):
                google_search(query)
            elif 'jarvis what time is it' in query:
                time()
            elif 'jarvis new prompt' in query:
                enterPrompt()
            elif 'jarvis power off' in query:
                say('Shutting down')
                exit()
            elif 'jarvis clear memory' in  query:
                memory = ''
            elif 'jarvis talk to me' in query:
                print('Chatting')
                chat()
            elif 'jarvis open' in query and 'located' in query:
                path = deal_with_query(query)
                print(path)
            elif 'jarvis read' in query and 'located' in query:
                path = deal_with_query(query)
                if(path):
                    vectorstore = vectorize(path)
                    if vectorstore:
                       print('vectorized') 
                       done_ques = ques_ans(vectorstore)
                    else:
                        say('System compromised, could nt read file')
                else:
                    say('No file found with that name, try again')
                continue 
            elif 'jarvis generate image' in query:
                imageGen = genImage.createImage()
                if imageGen:
                    say('Image generated and stored succesfully')
                        
            elif 'malf' not in query:
                say('I did not quite catch that, mind repeating it?')
                
