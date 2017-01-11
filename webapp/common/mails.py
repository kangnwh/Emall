from webapp.Models.db_basic import Session
from webapp.Models.user import User
from webapp.Models.email_advertisement import Email_advertisement
from flask_mail import Message
import flask_mail
mail = flask_mail.Mail()

def send_email_indiv(subject, recipients, text_body, html_body):
    msg = Message(subject=subject, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


def send_advertisement(ad):
    s = Session()
    recipients_result = s.query(User.email).filter(User.is_admin==0,User.valid_flg==1,User.is_subscribe==1).all()
    recipients = [x[0] for x in recipients_result]
    # ad = s.query(Email_advertisement).filter(Email_advertisement.email_advertisement_id == ad_id).first()
    msg = Message(subject=ad.title, recipients=recipients)
    # msg.body = text_body
    msg.html = ad.ad_content
    mail.send(msg)