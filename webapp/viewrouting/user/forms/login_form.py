from flask_wtf import Form
from wtforms import StringField,BooleanField,PasswordField
from wtforms.validators import DataRequired, ValidationError,EqualTo
from webapp.Models.user import User
from webapp.Models.db_basic import Session


def email_not_exists_check(self,field):
        session = Session()
        user = session.query(User).filter_by(email=self.email.data).first()
        session.close()
        if not user is None:
            raise ValidationError( 'Email %s is already exists !' % field.data )

def name_not_exists_check(self,field):
        session = Session()
        user = session.query(User).filter_by(email=self.email.data).first()
        if not user is None:
            raise ValidationError( 'User Name %s is already exists !' % field.data )

class LoginForm(Form):
    email = StringField('Email', validators = [DataRequired()])
    password = PasswordField('password', validators = [DataRequired()])
    remember_me = BooleanField('remember_me', default = False)
    next = StringField()

class ChangePasswordForm(Form):
    # email = StringField('Email', validators = [DataRequired()])
    password_old = PasswordField('Old Password', validators = [DataRequired()])
    password_new = PasswordField('New Password', validators = [DataRequired(), EqualTo('password_new_confirm', message='Passwords must match')])
    password_new_confirm = PasswordField('Confirm', validators = [DataRequired()])

    def get_user(self):
        session = Session()
        return session.query(User).filter_by(login=self.email.data).first()

#TODO need customized
class RegistrationForm(Form):
    email = StringField('Email', validators = [DataRequired(),email_not_exists_check])
    user_name = StringField('User Name', validators = [DataRequired(),name_not_exists_check])
    password = PasswordField('password', validators = [DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm  = PasswordField('Repeat Password')
    is_subscribe=BooleanField('Is Subscribe', default = False)
    next = StringField()