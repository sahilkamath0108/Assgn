import requests
import os
from dotenv import load_dotenv
load_dotenv()
import io
from PIL import Image
from helpers.say import say
from helpers.listen import listen

HG_FACE = os.getenv("HG_FACE")

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {HG_FACE}"}

def createImage():
    say('Enter prompt')
    prompt = listen()
    if prompt and 'malf' not in prompt:
        query = {
            'inputs' : prompt
        }
        response = requests.post(API_URL, headers=headers, json=query).content
        
        image = Image.open(io.BytesIO(response))
        file_path = f"C:\\Users\\Hp\\Desktop\\Code\\task\\assgn\\Assgn\\images\\{prompt[0:10]}.jpg"  
    
        image.save(file_path, exist_ok=True)
    return True


if __name__ == "__main__":
    createImage('Astroanut riding on a horse')