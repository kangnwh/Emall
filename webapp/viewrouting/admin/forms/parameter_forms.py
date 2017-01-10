from flask_wtf import Form
from wtforms import StringField,BooleanField,PasswordField,IntegerField,TextAreaField,DecimalField
from wtforms.validators import DataRequired, ValidationError,optional
from wtforms import validators
from webapp.Models.user import User
from webapp.Models.db_basic import Session

class ParameterForm(Form):
    REMINDER_PRE_DAYS = IntegerField('Reminder Before target date', validators = [DataRequired()])
    USER_POINT_DISCOUNT_RATE = DecimalField('User reward rate', validators = [DataRequired()])
    SHOW_HOT_PROD_NUM=IntegerField('SHOW HOT PROD NUMS', validators = [DataRequired()])
