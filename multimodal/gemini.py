import pathlib
import textwrap
import os
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown
import PIL.Image
import google.ai.generativelanguage as glm
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("gemini"))

model = genai.GenerativeModel('gemini-pro-vision')


def describe(path, desc):
    print(path, desc)
    img = PIL.Image.open(path)
    response = model.generate_content([desc, img], stream=True)
    response.resolve()
    print(response.text)
    return response.text

if __name__ == '__main__':
    describe("C:\\Users\\Hp\\Desktop\\Code\\flower.jpg")
