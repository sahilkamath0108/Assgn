import os
import openai
from dotenv import load_dotenv
load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from helpers.say import say

llm = ChatGoogleGenerativeAI(
    model="gemini-pro", verbose=True, temperature=0.7, google_api_key= os.getenv("GEMINI")
)

def return_answer(user_query):
        template = """
        You are a helpful assistant. Answer the following questions as accurately as possible:

        User question: {user_question}
        """

        prompt = ChatPromptTemplate.from_template(template)
        # llm = ChatOpenAI()
            
        chain = prompt | llm | StrOutputParser()
        
        return chain.invoke({
            "user_question": user_query,
        })
  

if __name__ == '__main__':
  say(return_answer('who is sam altman'))