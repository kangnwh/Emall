from flask_wtf import Form
from wtforms import StringField,IntegerField,DecimalField,DateField
from wtforms.validators import DataRequired
from wtforms import validators


class UserOrderForm(Form):
    #basic info
    prod_id = IntegerField("Prod Id",validators=[DataRequired()])
    prod_name = StringField('Production Name', validators = [DataRequired()])
    prod_quantity = IntegerField("Quantity",validators=[DataRequired()])
    lead_time = StringField('Lead Time')
    prod_size = StringField('Production Size')
    imprint_info = StringField('Imprint Size')
    colors = StringField('Colors')

    #money info
    unit_price = DecimalField("Unit Price",validators=[DataRequired()])
    imprinting_prices = DecimalField("Unit Price",validators=[DataRequired()])
    setup_cost = DecimalField("Unit Price",validators=[DataRequired()])
    freight_cost = DecimalField("Unit Price",validators=[DataRequired()])
    total_price = DecimalField("Unit Price",validators=[DataRequired()])
    #need_pay_supplier should be calculated

    #order flag
    supplier_checked_flg = IntegerField("Supplier Checked Flag")
    supplier_target_dt = DateField("Unit Price",validators=[DataRequired()]) #this should be calculated
    #is_remind = IntegerField("Unit Price",validators=[DataRequired()])
    #order_stat = IntegerField("Supplier Checked Flag") should be settled in code

    #comments
    #user_comments = StringField("Comments")
    supplier_comments = StringField("Comments")
