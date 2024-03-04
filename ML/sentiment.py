import os
from dotenv import load_dotenv
load_dotenv()

HG_FACE = os.getenv("HG_FACE")

import requests

API_URL = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment-latest"
headers = {"Authorization": f"Bearer {HG_FACE}"}

def pred_sent(sentence):
    response = requests.post(API_URL, headers=headers, json=sentence)
    return response.json()[0][0]



if __name__ == "__main__":
    output = pred_sent({
	"inputs": "yeah yeah",
    })

    print(output)