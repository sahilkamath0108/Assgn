from langchain_community.vectorstores import Chroma
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM 
from transformers import pipeline
import torch
from langchain_community.llms import HuggingFacePipeline
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.chains import RetrievalQA
from helpers.say import say
from helpers.listen import listen
from langchain.chains import ConversationalRetrievalChain
from langchain_google_genai import ChatGoogleGenerativeAI
import os

chat_history = []
llm = ChatGoogleGenerativeAI(
    model="gemini-pro", verbose=True, temperature=0.7, google_api_key= os.getenv("GEMINI"), convert_system_message_to_human=True
)


def ques_ans(vectorstore):
    global db
    db = vectorstore
    say('Alright shoot questions at me')
    while True:
        query = listen()
        if 'malf' in query:
            continue
        if 'finish questioning' in query:
            break
        else:
            if query and 'malf' not in query:
                response = chat(chat_history, query)
                say(response)
                say('Next question')
    return True
            

def chat(chat_history, user_input):
    
    qa = ConversationalRetrievalChain.from_llm(llm, retriever=db.as_retriever())
    

    bot_response = qa.invoke({"question":user_input, "chat_history":chat_history})
    bot_response = bot_response['answer']
    response = ""
    for letter in ''.join(bot_response):
        response += letter + ""
        chat_history = chat_history + [(user_input, response)]
    return bot_response

checkpoint = "MBZUAI/LaMini-Flan-T5-783M"     #google/flan-t5-xl  google/flan-t5  MBZUAI/LaMini-Flan-T5-783M
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
base_model = AutoModelForSeq2SeqLM.from_pretrained(
    checkpoint,
    device_map="auto",
    offload_folder="offload",
    torch_dtype = torch.float32)

pipe = pipeline(
    'text2text-generation',
    model = base_model,
    tokenizer = tokenizer,
    max_length = 512,
    do_sample = True,
    temperature = 0.3,
    top_p= 0.95
)
local_llm = HuggingFacePipeline(pipeline=pipe)


if __name__ == "__main__":
    ques_ans('meaning of didactic')

