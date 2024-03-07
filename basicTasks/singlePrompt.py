#helper modules
from helpers.listen import listen
from helpers.say import say

import os
import promptFile
import pyperclip

def enterPrompt():
    say('Yes sir, go ahead')
    prompt = listen()
    prompt = prompt.lower()
    response = promptFile.return_answer(prompt)
    
    token = response.split()
    to_be_said = response.split('.')[0:3] 
    say(to_be_said)
        
    if(len(token) > 30):
        say('Would you like to copy the rest of the answer to clipboard?')
        resp = listen().lower()
        if resp == 'yes do that':
            pyperclip.copy(response)
            say('Copied')
    
    if not os.path.exists('prompt_answers'):
        os.mkdir('prompt_answers')
    
    with open(f'prompt_answers/{prompt}', 'w') as f:
        f.write(response)