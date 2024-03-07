import os
from dotenv import load_dotenv
load_dotenv()

HG_FACE = os.getenv("HG_FACE")

import requests

# API_URL = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment-latest"
# headers = {"Authorization": f"Bearer {HG_FACE}"}

# def pred_sent(sentence):
#     response = requests.post(API_URL, headers=headers, json=sentence)
#     return response.json()[0][0]

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
sid_obj = SentimentIntensityAnalyzer()
 
def sentiment_scores(sentence):

    sentiment_dict = sid_obj.polarity_scores(sentence)
    
    if sentiment_dict['compound'] >= 0.05 :
        return False
    elif sentiment_dict['compound'] <= - 0.05 :
        return True



if __name__ == "__main__":
    print(sentiment_scores('what good is the time'))