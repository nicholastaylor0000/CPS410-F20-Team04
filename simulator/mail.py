import requests
from .settings import MAILGUN_API_KEY, MAILGUN_DOMAIN, HOST
from django.urls import reverse

def send_email(to, subject, body):
    return requests.post(
        f'https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages',
        auth=('api', MAILGUN_API_KEY),
        data={'from': f'Museum Tracker <mailgun@{MAILGUN_DOMAIN}>',
            'to': [to],
            'subject': subject,
            'text': body,
        }
    )

def send_pass_email(to, token):
    request = send_email(
        to,
        'password reset',
        'A password reset has been requested for your account \n'
        'go to this link: ' + HOST + reverse('password_reset_confirm', args=[token]),
    )
    return request.status_code

def send_confirm_email(to, token):
    request = send_email(
        to, 
        'account confirmation',
        'go to this link to confirm your account \n' + 
        HOST + reverse('confirm-account', args=[token]),
    )
    return request.status_code