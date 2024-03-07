#Sentiment
from ML import sentiment

#deal with files
from deal_with_files.open_file import deal_with_query
from deal_with_files.vecDB import vectorize
from deal_with_files.performQA import ques_ans

#helper modules
from helpers.listen import listen
from helpers.say import say

#gen image
from ML import genImage
from multimodal import gemini

#basic tasks
from basicTasks import youtube, search, time, chatbot, singlePrompt, sendMail

    
if __name__ == '__main__':
    print('hi')
    say('Jarvis activated')
    
    while True:
        print('Listening')
        query = listen()
        query = query.lower()
        if query:
            print(query)
            if(sentiment.sentiment_scores(query)):
                say("You seem to be angry sir! Calm down")   
            if 'jarvis play' in query:
                youtube.youtube_video(query)
            elif query.startswith('jarvis search') and query.endswith('on google'):
                search.google_search(query)
            elif 'jarvis what time is it' in query:
                time.time()
            elif 'jarvis new prompt' in query:
                singlePrompt.enterPrompt()
            elif 'jarvis send email' in query:
                sendMail.sendEmail()
            elif 'jarvis power off' in query:
                say('Shutting down')
                exit()
            elif 'jarvis talk to me' in query:
                print('Chatting')
                chatbot.chat()
            elif 'jarvis open' in query and 'located' in query:
                path = deal_with_query(query)
            elif 'jarvis read' in query and 'located' in query:
                deal_with_query(query)
                continue 
            elif 'jarvis generate image' in query:
                genImage.createImage()
            elif 'jarvis describe image' in query:
                gemini.describe()
                        
            elif 'malf' not in query:
                say('I did not quite catch that, mind repeating it?')