import smtplib
import random
import string
from passlib.hash import pbkdf2_sha256
from email.mime.text import MIMEText
from email.header import Header
from .constants import host, port, email, password, password_length, email_subject, email_body


def generate_password():
    characters = string.ascii_letters + string.digits
    user_password = ''.join(random.choice(characters) for _ in range(password_length))
    return user_password


def send_message(receiver: str, message: MIMEText):
    server = smtplib.SMTP(host, port)
    server.ehlo(email)
    server.starttls()
    server.login(email, password)
    server.auth_plain()
    print(message.as_string())
    server.sendmail(email, receiver, message.as_string())
    server.quit()


def form_user_password(login: str):
    user_password = generate_password()
    msg = MIMEText(email_body.format(user_password), 'plain', 'utf-8')
    msg['Subject'] = Header(email_subject, 'utf-8')
    msg['From'] = email
    msg['To'] = login
    send_message(login, msg)
    return pbkdf2_sha256.hash(user_password)

