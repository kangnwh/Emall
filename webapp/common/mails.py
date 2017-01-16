from webapp.Models.db_basic import Session
from webapp.Models.user import User
from webapp.common import get_host_info
from flask_mail import Message
from flask import current_app
import flask_mail, urllib

mail = flask_mail.Mail()

emall_ip, emall_port = get_host_info('HOME_HOST')
emall_host = "http://{emall_ip}:{emall_port}".format(emall_ip=emall_ip,emall_port = emall_port )


def send_email_base(subject, recipients, html_body, cc_list=None):
    msg = Message(subject=subject, recipients=recipients, cc=cc_list)
    msg.body = None
    msg.html = html_body
    mail.send(msg)


def email_notifier(email, subject, html):
    send_email_base(subject, email, html_body=html, cc_list=current_app.config.get("ADMIN_EMAIL"))


# def order_notifier_to_supplier(order,subject,email):
#     user_notification = order.notification_to_user()
#     send_email_base(subject, supplier_email, html_body=user_notification, cc_list=current_app.config.get("ADMIN_EMAIL"))

def deliver_notification():
    try:
        print("Sending Deliver Notification...")
        result = urllib.request.urlopen("{host}/admin/deliver_notification".format(host=emall_host))
    except:
        print("Send Deliver Notification Failed")
    return result


def send_advertisement(ad):
    s = Session()
    recipients_result = s.query(User.email).filter(User.is_admin == 0, User.valid_flg == 1,
                                                   User.is_subscribe == 1).all()
    recipients = [x[0] for x in recipients_result]
    # ad = s.query(Email_advertisement).filter(Email_advertisement.email_advertisement_id == ad_id).first()
    msg = Message(subject=ad.title, recipients=recipients)
    # msg.body = text_body
    msg.html = ad.ad_content
    mail.send(msg)
