import os

from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

from dotenv import load_dotenv



load_dotenv()

SID = os.getenv("SID")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
WA_TWILIO = os.getenv("WA_TWILIO")
WA_TIM = os.getenv("WA_TIM")
WA_BEN = os.getenv("WA_BEN")




def send_wa(message, to):

    proxy_client = TwilioHttpClient(proxy={'http': os.environ['http_proxy'], 'https': os.environ['https_proxy']})

    client = Client(SID, AUTH_TOKEN, http_client=proxy_client)

    client.messages.create(body=message, from_=WA_TWILIO, to=to)



def msg_tim(msg):
    send_wa(msg, WA_TIM)

def msg_ben(msg):
    send_wa(msg, WA_BEN)