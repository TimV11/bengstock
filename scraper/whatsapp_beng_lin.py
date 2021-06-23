import os

from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient




def send_wa(message):

    account_sid = 'AC41248ad25d305b06fe97c70ca704cdfb'
    auth_token = 'b1416a829398f7e41ab5bb8619e63c8b'

    proxy_client = TwilioHttpClient(proxy={'http': os.environ['http_proxy'], 'https': os.environ['https_proxy']})
    client = Client(account_sid, auth_token, http_client=proxy_client)

    from_whatsapp_number = "whatsapp:+14155238886"
    to_whatsapp_number = "whatsapp:+4915233661319"

    client.messages.create(body = message, from_ = from_whatsapp_number, to = to_whatsapp_number)