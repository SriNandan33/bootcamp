from threading import Thread
from flask import render_template, current_app
from flask_mail import Message
from app.email import send_email

def send_password_reset_email(user):
    token = user.get_password_reset_token()
    send_email(
        "[Bootcamp] Reset your password",
        sender=current_app.config["ADMIN_EMAIL"],
        recipients=[user.email],
        text_body=render_template('auth/email/reset_password.txt', user=user, token=token),
        html_body=render_template('auth/email/reset_password.html', user=user, token=token)
    )