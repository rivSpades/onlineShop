# utils.py

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings

def send_activation_email(user, domain):
    mail_subject = 'Activate your account'
    message = render_to_string('accounts/account_verification_email.html', {
        'user': user,
        'domain': domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    email = EmailMessage(mail_subject, message, to=[user.email])
    email.send()

def send_password_reset_email(user, request):
    mail_subject = 'Password Reset Request'
    domain = request.get_host()
    message = render_to_string('accounts/reset_password_email.html', {
        'user': user,
        'domain': domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    email = EmailMessage(mail_subject, message, to=[user.email])
    email.send()
