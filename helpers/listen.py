import speech_recognition as sr
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.5
        audio = r.listen(source, timeout=30)  # Wait for up to 10 seconds for input
        try:
            query = r.recognize_google(audio, language='en-in')
            print(query)
            return query
        except sr.WaitTimeoutError:
            print('timeout')
            return 'error'
        except Exception as e:
            print('malf')
            return 'malf'
        
if __name__ == '__main__':
    query = listen()
    print(query)
    