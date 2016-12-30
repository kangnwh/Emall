# -*- coding: utf-8 -*-
import webapp
import os

# upload folder
PROD_UPLOAD_PATH = "{base_dir}{sep}static{sep}img{sep}products{sep}".format(base_dir=os.path.dirname(webapp.__file__), sep=os.sep)
USER_LOGO_UPLOAD_PATH = "{base_dir}{sep}static{sep}img{sep}user_logos{sep}".format(base_dir=os.path.dirname(webapp.__file__), sep=os.sep)

PROD_NUM_PER_PAGE = 9
USER_NUM_PER_PAGE = 20
FEEDBACK_NUM_PER_PAGE = 10
USER_ORDER_PER_PAGE = 20
USER_QUOTE_PER_PAGE = 20

ALLOWED_EXTENSIONS=set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','TXT', 'PDF', 'PNG', 'JPG', 'JPEG', 'GIF'])


MAIL_SERVER = 'smtp.tom.com'# 'smtp.163.com'
MAIL_PORT = 25
MAIL_USE_SSL = False
MAIL_USE_TLS = False
MAIL_USERNAME = 'emalltest'
MAIL_DEFAULT_SENDER = 'emalltest@tom.com'
MAIL_PASSWORD = 'passw0rd'

# user discount rate
USER_POINT_DISCOUNT_RATE = 0.01
#Reminders should be sent %d days before end date
REMINDER_PRE_DAYS = 3

ORDER_STATUS_MAP={
    #0:'default',
    1:'User Submitted',
    2:'Supplier Checked',
    3:'Product On The Way',
    4:'User Feedback Submitted',
    5:'Finished',
    6:'User Canceled',
    7:'Supplier Canceled'
}

QUOTE_STATUS_MAP={
    0:'User Submitted',
    1:'Supplier Replied'
}

APPROVAL_STATUS_MAP={
    -1:"Rejected",
    0:"Pending",
    1:"Approved"
}

RATE_NOTIFICATION="There will be an add-up rate when users buy this product."