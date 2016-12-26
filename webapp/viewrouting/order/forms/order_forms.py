from flask_wtf import Form
from wtforms import StringField,IntegerField,DecimalField,DateField
from wtforms.validators import DataRequired
from wtforms import validators


class UserOrderForm(Form):
    ##TODO
    #basic info
    supplier_id = IntegerField("Supplier ID",validators=[DataRequired()])
    prod_id = IntegerField("Prod Id",validators=[DataRequired()])
    prod_name = StringField('Production Name', validators = [DataRequired()])
    prod_quantity = IntegerField("Quantity",validators=[DataRequired()]) #user
    lead_time = StringField('Lead Time')
    prod_size = StringField('Production Size')
    imprint_info = StringField('Imprint Info') #user
    colors = StringField('Color',validators=[DataRequired()]) #user

    #money info
    unit_price = DecimalField("Unit Price",validators=[DataRequired()]) #user
    imprinting_prices = DecimalField("Imprinting Price",validators=[DataRequired()]) #user
    setup_cost = DecimalField("Setup Cost",validators=[DataRequired()]) #user
    freight_cost = DecimalField("Freight Cost",validators=[DataRequired()]) #user
    total_price = DecimalField("Total Price",validators=[DataRequired()]) #user
    #need_pay_supplier should be calculated
    is_used_points = IntegerField("Do you want to use your points?")
    used_points = IntegerField("How many to use?")

    #order flag
    #supplier_checked_flg = IntegerField("Supplier Checked Flag")
    #supplier_target_dt = DateField("Supplier Target Date",validators=[DataRequired()]) #supplier
    #is_remind = IntegerField("Unit Price",validators=[DataRequired()])
    #order_stat = IntegerField("Supplier Checked Flag") should be settled in code

    #comments
    user_comments = StringField("Comments")
    #supplier_comments = Column(String(500)) should be input when supplier handle this order
