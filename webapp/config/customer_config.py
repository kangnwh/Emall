import webapp
import os

# upload folder
PROD_UPLOAD_PATH = "{base_dir}{sep}static{sep}img{sep}products{sep}".format(base_dir=os.path.dirname(webapp.__file__), sep=os.sep)
USER_LOGO_UPLOAD_PATH = "{base_dir}{sep}static{sep}img{sep}user_logos{sep}".format(base_dir=os.path.dirname(webapp.__file__), sep=os.sep)

PROD_NUM_PER_PAGE = 9
USER_NUM_PER_PAGE = 10
FEEDBACK_NUM_PER_PAGE = 10

ALLOWED_EXTENSIONS=set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','TXT', 'PDF', 'PNG', 'JPG', 'JPEG', 'GIF'])


MAIL_SERVER = 'smtp.tom.com'# 'smtp.163.com'
MAIL_PORT = 25
MAIL_USE_SSL = False
MAIL_USE_TLS = False
MAIL_USERNAME = 'emalltest'
MAIL_DEFAULT_SENDER = 'emalltest@tom.com'
MAIL_PASSWORD = 'passw0rd'
