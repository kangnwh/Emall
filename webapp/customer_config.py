import webapp
import os

# upload folder
PROD_UPLOAD_PATH = "{base_dir}{sep}static{sep}img{sep}products{sep}".format(base_dir=os.path.dirname(webapp.__file__), sep=os.sep)
USER_LOGO_UPLOAD_PATH = "{base_dir}{sep}static{sep}img{sep}user_logos{sep}".format(base_dir=os.path.dirname(webapp.__file__), sep=os.sep)

PROD_NUM_PER_PAGE = 9
USER_NUM_PER_PAGE = 10
FEEDBACK_NUM_PER_PAGE = 10

ALLOWED_EXTENSIONS=set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','TXT', 'PDF', 'PNG', 'JPG', 'JPEG', 'GIF'])