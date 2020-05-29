
import random
from twilio.rest import Client
import re

from django.utils import timezone
from datetime import datetime, timedelta, date


account_sid = 'ACbd44dd22794ad8e0268615ea28eca6fa'
auth_token = 'd4e874adeace90e6cecdc46fb3ca450c'
twilio = '+15005550006'


def send_otp_user(name, recv):        
    my = recv    
    name = name
    client = Client(account_sid, auth_token)
    otp = random.randint(111111, 999999)    
    my_msg = "Hi " + name + " !" + "\n" + "Your Night Market account verification otp is : " + str(otp)
    message = client.messages.create(body=my_msg, from_=twilio, to=my)  
    return otp
