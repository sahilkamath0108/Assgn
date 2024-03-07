#helper modules
from helpers.listen import listen
from helpers.say import say

import datetime

def time():
    time = datetime.datetime.now().strftime('%H:%M:%S')
    say(f'Sir, the time is {time}')