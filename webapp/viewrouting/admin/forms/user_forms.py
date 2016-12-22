from flask_wtf import Form
from wtforms import StringField,BooleanField,PasswordField,IntegerField,TextAreaField,DecimalField
from wtforms.validators import DataRequired, ValidationError,optional
from wtforms import validators
from webapp.Models.user import User
from webapp.Models.db_basic import Session


def email_not_exists_check(self,field):
        session = Session()
        if not session.query(User).filter_by(email=self.email.data).first() is None:
            raise ValidationError( 'Email %s is already exists !' % field.data )

def name_not_exists_check(self,field):
        session = Session()
        if not session.query(User).filter_by(email=self.email.data).first() is None:
            raise ValidationError( 'User Name %s is already exists !' % field.data )

class CreateNewForm(Form):
    user_name = StringField('User Name', validators = [DataRequired(),name_not_exists_check])
    email = StringField('Email', validators = [DataRequired(),email_not_exists_check])
    password = PasswordField('Password', validators = [DataRequired()])
    valid_flg=BooleanField('Is Valid', default = False)
    is_admin = BooleanField('Is Admin', default = False)
    is_subscribe=BooleanField('Is Subscribe', default = False)


class UpdateUserForm(Form):
    user_id = StringField("User ID", validators = [DataRequired()])
    # user_name = StringField('User Name', validators = [DataRequired()])
    # email = StringField('Email', validators = [DataRequired()])
    # password = PasswordField('Password', validators = [DataRequired()])
    is_admin = BooleanField('Is Admin', default = False)
    valid_flg = BooleanField('Is Valid', default = False)
    logo_link = StringField('Logo Link')


class DeleteUserForm(Form):
    user_id = IntegerField('UserID', validators = [DataRequired()])


class ResetPassForm(Form):
    user_id = StringField("User ID", validators = [DataRequired()])
    email = StringField('Email')
    password = PasswordField('Password')
