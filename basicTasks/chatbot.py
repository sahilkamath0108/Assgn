#helper modules
from helpers.listen import listen
from helpers.say import say

import promptFile

memory = ''

import sqlite3

db_file = "chat_history.db"

def initialize_database():
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS chat_history
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, conversation TEXT)''')

    conn.commit()
    conn.close()

def insert_chat_history(conversation):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    c.execute("INSERT INTO chat_history (conversation) VALUES (?)", (conversation,))
    conn.commit()
    conn.close()

def retrieve_chat_history():
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("SELECT conversation FROM chat_history")
    chat_history = c.fetchall()

    conn.close()
    return chat_history

initialize_database()

def chat():
    count = 0
    conversation = []

    say('What can I help you with?')
    chat_h = retrieve_chat_history()

    while count != 1:
        query = listen().lower()
        if 'error' in query or 'malf' in query:
            continue
        if 'jarvis quit chatting' in query:
            exit()
        
        chat_h.append(f"User: {query}")
        
        response = promptFile.return_answer(query)

        print(response)
        chat_h.append(f"AI: {response}")

        insert_chat_history("\n".join(chat_h))

        say(response)

    return 'Nice talking with you sir!'

if __name__ == '__main__':
    chat()
