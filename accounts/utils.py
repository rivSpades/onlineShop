# utils.py

from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, Content
import os

def send_activation_email(user, domain):
    # Prepare email content
    mail_subject = 'Activate your account'
    message = render_to_string('accounts/account_verification_email.html', {
        'user': user,
        'domain': domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    
    # Create the email
    email = Mail(
        from_email=os.environ.get('DEFAULT_FROM_EMAIL'),  # Replace with a verified SendGrid sender email
        to_emails=user.email,
        subject=mail_subject,
        html_content=message)
    

    # Send the email using SendGrid API
    try:
        
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(email)
        print(response.status_code)  # Useful for debugging
    except Exception as e:
        print(f"Error sending email: {e}")


def send_password_reset_email(user, request):
    mail_subject = 'Password Reset Request'
    domain = request.get_host()
    message = render_to_string('accounts/reset_password_email.html', {
        'user': user,
        'domain': domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    
    # Create the email
    email = Mail(
        from_email=Email(settings.DEFAULT_FROM_EMAIL),
        to_emails=user.email,
        subject=mail_subject,
        html_content=message
    )

    # Send the email using SendGrid API
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(email)
        print(response.status_code)  # Useful for debugging
    except Exception as e:
        print(f"Error sending email: {e}")
