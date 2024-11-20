# utils.py

from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, Content
import os

def send_order_email(user, order):
    # Prepare email content
    mail_subject = 'Thank you for your order'
    message = render_to_string('orders/order_received_email.html', {
        'user': user,
        'order': order,

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


