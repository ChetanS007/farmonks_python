from django.core.mail import send_mail
from datetime import datetime
from twilio.rest import Client
import secrets
from decouple import config
from sms import send_sms
import requests
from .config import *
from django.core.cache import cache

def send_email_to_user(request,email,email_token):

    try:
        subject = 'This is a test email.'
        message = f'Click on the link to verify http://127.0.0.1:8000/verify/{email_token}'
        recipient_list = [email]

        send_mail(subject, message, 'sender_email@example.com', recipient_list)
    except Exception as e:

        return False
    
    return True

#need to be in text sms...
def sms_otp_to_user(request,phone):

        try:
            api_key= config('API_KEY')
            otp = ''.join(secrets.choice('0123456789') for _ in range(6))
            cache.set("OTP", otp)
            url = f'https://2factor.in/API/V1/{api_key}/SMS/{phone}/{otp}'  

            response = requests.get(url)
            print(response)
        except Exception as e:
            print(e)

       