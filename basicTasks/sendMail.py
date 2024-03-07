import os
from dotenv import load_dotenv
load_dotenv()

from helpers.say import say
from helpers.listen import listen

import smtplib, ssl

SMTP_SERVER = "smtp.gmail.com"
PORT = 587
EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')

context = ssl.create_default_context()

def sendEmail():
    say('Enter recipient address')
    to = input('Enter recipient address')
    say('Enter subject')
    subject = listen()
    
    say('Enter message')
    message = listen()
    
    with smtplib.SMTP(SMTP_SERVER, PORT) as server:
        server.starttls(context=context)
        server.login(EMAIL, PASSWORD)
        message = f"""\
        Subject: {subject}

        {message}
        """
        server.sendmail(EMAIL, to, message)
        say('Email sent successfully')


