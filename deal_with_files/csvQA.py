import tabulate
import pandas as pd
from langchain_community.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain_experimental.agents import create_csv_agent
from langchain.agents.agent_types import AgentType
import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
file_path= 'C:\\Users\\Hp\\Desktop\\archive\\tested.csv'

csv_agent= create_csv_agent(
        ChatOpenAI(temperature=0, model="gpt-4", openai_api_key='OPENAI_API_KEY'),
        file_path, 
        verbose=True,
        stop=["\nObservation:"],
        agent_type=AgentType.OPENAI_FUNCTIONS,
        handle_parsing_errors=True
    )
    
csv_agent.run("What is the csv file about?")