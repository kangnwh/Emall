
from flask_mail import Message
from webapp.Report import mail

def send_email_indiv(subject, recipients, text_body, html_body):
    msg = Message(subject=subject, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


def send_batch():
    pass