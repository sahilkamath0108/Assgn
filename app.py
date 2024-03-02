import streamlit as st
import os
import sqlite3
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()
from PIL import Image
import requests
from io import BytesIO
import tempfile
from RAG import csvRag
from langchain.chains import ConversationalRetrievalChain
from langchain.chains import RetrievalQA 


llm = ChatGoogleGenerativeAI(
    model="gemini-pro", verbose=True, temperature=0.7, google_api_key=os.getenv("gemini"), convert_system_message_to_human=True
)

HG_FACE = os.getenv("HG_FACE")

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {HG_FACE}"}

os.environ["OPENAI_API_BASE"]='http://localhost:1234/v1'
os.environ["OPENAI_MODEL_NAME"]='zephyr'
os.environ["OPENAI_API_KEY"]='not-needed'

load_dotenv()

st.set_page_config(page_title="Streaming bot", page_icon="🤖")

# Function to create SQLite connection and table
def create_connection(database):
    conn = None
    try:
        conn = sqlite3.connect(database)
        c = conn.cursor()
        c.execute('''
                  CREATE TABLE IF NOT EXISTS chat_history (
                      id INTEGER PRIMARY KEY,
                      content TEXT,
                      message_type TEXT
                  )
                  ''')
    except sqlite3.Error as e:
        print(e)
    return conn

# Define file path for SQLite database
database_path = "session_state.db"

# Initialize SQLite connection
conn = create_connection(database_path)

selected_page = st.sidebar.selectbox("Select a page", ["Home", "Chat", "Gen Image", "RAG"])

if selected_page == "Home":
    st.title("Home Page")
    st.write("Welcome to the home page!")
elif selected_page == "Chat":
    st.title("Chat Page")
    
    def get_response(user_query, chat_history):

        template = """
        You are a helpful assistant. Answer the following questions considering the history of the conversation:

        Chat history: {chat_history}

        User question: {user_question}
        """

        prompt = ChatPromptTemplate.from_template(template)
        # llm = ChatOpenAI()
            
        chain = prompt | llm | StrOutputParser()
        
        return chain.stream({
            "chat_history": chat_history,
            "user_question": user_query,
        })

    # Load chat history from SQLite database
    chat_history = []
    if conn is not None:
        c = conn.cursor()
        c.execute("SELECT content, message_type FROM chat_history ORDER BY id")
        rows = c.fetchall()
        for row in rows:
            if row[1] == 'AI':
                chat_history.append(AIMessage(content=row[0]))
            else:
                chat_history.append(HumanMessage(content=row[0]))
    
    # Display conversation history
    for message in chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.write(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.write(message.content)

    # User input
    user_query = st.chat_input("Type your message here...")
    if user_query is not None and user_query != "":
        # Add user message to chat history and save to database
        chat_history.append(HumanMessage(content=user_query))
        if conn is not None:
            c = conn.cursor()
            c.execute("INSERT INTO chat_history (content, message_type) VALUES (?, ?)", (user_query, 'Human'))
            conn.commit()

        with st.chat_message("Human"):
            st.markdown(user_query)

        # Get AI response
        response = st.write_stream(get_response(user_query, chat_history))
        chat_history.append(AIMessage(content=response))

        # Save AI response to database
        if conn is not None:
            c = conn.cursor()
            c.execute("INSERT INTO chat_history (content, message_type) VALUES (?, ?)", (response, 'AI'))
            conn.commit()

    # Close SQLite connection
    if conn is not None:
        conn.close()
elif selected_page == "Gen Image":
    st.header("🖼️Image generation🖼️")
    
    user_query = st.chat_input("Type your prompt for image generation: ")
    
    if user_query:
        with st.spinner("Generating image..."):

            image_bytes = requests.post(API_URL, headers=headers, json=user_query).content

            image = Image.open(BytesIO(image_bytes))

        st.image(image, caption='Generated Image', use_column_width=True)
elif selected_page == "RAG":
    st.header("📝RAG")
    
    uploaded_file = st.file_uploader("Upload a CSV or PDF file", type=['csv', 'pdf'])

    if uploaded_file is not None:

        file_extension = uploaded_file.name.split(".")[-1]
        if file_extension == "csv":
            st.success("File type: CSV")
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name
                
            vectorstore = csvRag.processCSV(tmp_file_path)
            
            if vectorstore:
                qa = ConversationalRetrievalChain.from_llm(llm, retriever=vectorstore.as_retriever())
                query = st.text_input("Enter query: ")
                if query:
                    chat_history = []
                    result = qa.invoke({"question":query, "chat_history":chat_history})
                    print("Response: ", result['answer'])
                    chat_history.append(result['answer'])
                    st.write(result['answer'])

                
        elif file_extension == "pdf":
            st.success("File type: PDF")
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name
                
            vectorstore = csvRag.processPDF(tmp_file_path)
            
            if vectorstore:
                qa = ConversationalRetrievalChain.from_llm(llm, retriever=vectorstore.as_retriever())
                query = st.text_input("Enter query: ")
                if query:
                    chat_history = []
                    result = qa.invoke({"question":query, "chat_history":chat_history})
                    print("Response: ", result['answer'])
                    chat_history.append(result['answer'])
                    st.write(result['answer'])


