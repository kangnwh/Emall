from flask_wtf import Form
from wtforms import StringField,BooleanField,TextAreaField,FileField
from wtforms.validators import DataRequired
from wtforms import validators


class UserFeedbackForm(Form):
    valid_flg=BooleanField('Is Valid', default = False)
    user_id = StringField("User ID", validators = [DataRequired()])
    user_name = StringField('User Name', validators = [DataRequired()])
    email = StringField('Email', validators = [DataRequired()])
    user_comment = TextAreaField('User Comment',validators = [DataRequired(),validators.length(max=3000)])

class UploadUserLogoForm(Form):
    user_logo_file = FileField('Upload Your Logo')