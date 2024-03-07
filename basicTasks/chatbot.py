#helper modules
from helpers.listen import listen
from helpers.say import say

import promptFile

memory = ''

def chat():
    global memory
    count = 0
    say('What can I help you with?')
    while count != 1:
        query = listen().lower()
        if 'error' in query or 'malf' in query:
            continue
        if 'jarvis quit chatting' in query:
            count = 1
        memory += f'Sahil : {query}\n Jarvis: '
        response = promptFile.return_answer(memory)
        say(response)
        memory += f'{response}\n'
    return 'Nice talking with you sir!'