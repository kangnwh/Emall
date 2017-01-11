from flask_wtf import Form
from wtforms import StringField,IntegerField,DecimalField,DateField
from wtforms.validators import DataRequired
from wtforms import validators


class AdForm(Form):
    #basic info
    title = StringField("Subject",validators=[DataRequired()])
    ad_content = StringField('Ad content', validators = [DataRequired()])

