from threading import Thread
from flask import current_app
from app import mail
from sendgrid.helpers.mail import Mail

def send_async_email(app, msg):
    with app.app_context():
        try:
            response = mail.send(msg)
        except Exception as e:
            print(e)

def send_email(subject, sender, recipients, html_body):
    msg = Mail(
        from_email = sender,
        to_emails = recipients,
        subject = subject,
        html_content = html_body
    )
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()