from webapp.Models.db_basic import Session
from webapp.Models.user import User
from webapp.Models.email_advertisement import Email_advertisement
from flask_mail import Message
from flask_login import current_user
from flask import current_app
import flask_mail
mail = flask_mail.Mail()

def send_email_base(subject, recipients, html_body, cc_list=None):
    msg = Message(subject=subject, recipients=recipients,cc=cc_list)
    msg.body = None
    msg.html = html_body
    mail.send(msg)

def email_notifier(email, subject, html):
    send_email_base(subject, email, html_body=html, cc_list=current_app.config.get("ADMIN_EMAIL"))


# def order_notifier_to_supplier(order,subject,email):
#     user_notification = order.notification_to_user()
#     send_email_base(subject, supplier_email, html_body=user_notification, cc_list=current_app.config.get("ADMIN_EMAIL"))

def deliver_notification():
    send_email_base("deliver_notification",["792564101@qq.com"],"schedule test")

def send_advertisement(ad):
    s = Session()
    recipients_result = s.query(User.email).filter(User.is_admin==0,User.valid_flg==1,User.is_subscribe==1).all()
    recipients = [x[0] for x in recipients_result]
    # ad = s.query(Email_advertisement).filter(Email_advertisement.email_advertisement_id == ad_id).first()
    msg = Message(subject=ad.title, recipients=recipients)
    # msg.body = text_body
    msg.html = ad.ad_content
    mail.send(msg)