import requests
import json
import smtplib
import logging

URL = 'https://v2.jokeapi.dev/joke/Programming?blacklistFlags=nsfw,religious,political,racist,sexist,explicit'

with open('creds.json', 'r') as f:
    creds = json.load(f)
    f.close()

LOGFILE = 'email_send.log'
EMAIL = creds['email']
PASSWORD = creds['password']
RECIPIENT = EMAIL

logging.basicConfig(filemode = 'a', filename=LOGFILE, level=logging.INFO, format='%(levelname)s - %(asctime)s - %(message)s')

def send_email(joke):
  
    try:
        s = smtplib.SMTP('smtp.gmail.com', 587) #SPECIFIC TO GMAIL
        s.starttls() #encryption
    except smtplib.SMTPConnectError:
        logging.error('could not connect to the mail server')

    try:
        s.login(EMAIL,PASSWORD)
    except smtplib.SMTPAuthenticationError:
        logging.error('Auth Failure')

    try:
        s.sendmail(EMAIL, RECIPIENT, f'\n{joke}') #from, to, content
    except smtplib.SMTPException:
        logging.error('Unable to send email due to error')
        exit()
    s.quit()


def get_joke_content():
    response = requests.get(URL)
    result = response.json()
    if result['error']:
        logging.error('something went wrong with the request to the API')
        return None
    if result['type'] == 'twopart':
        setup = result['setup']
        delivery = result['delivery']
        return f'setup: {setup}\n delivery: {delivery}'
    else:
        joke = result['joke']
        return f'Joke: {joke}'

#start of program execution 
joke = get_joke_content()
logging.info('Joke retreived successfully!')
if joke is not None:
    send_email(joke)
    logging.info('email sent successfully!')
