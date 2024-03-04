import win32com.client

speaker = win32com.client.Dispatch('SAPI.SpVoice')

def say(text):
    speaker.Speak(text)
    
if __name__ == '__main__':
    say("Hello World")