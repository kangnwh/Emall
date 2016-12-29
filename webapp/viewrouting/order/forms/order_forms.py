from flask_wtf import Form
from wtforms import StringField,IntegerField,DecimalField,DateField,BooleanField
from wtforms.validators import DataRequired
from wtforms import validators


class UserOrderForm(Form):
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
    # unit_price = DecimalField("Unit Price",validators=[DataRequired()]) #user
    # imprinting_prices = DecimalField("Imprinting Price",validators=[DataRequired()]) #user
    # setup_cost = DecimalField("Setup Cost",validators=[DataRequired()]) #user
    # freight_cost = DecimalField("Freight Cost",validators=[DataRequired()]) #user
    # total_price = DecimalField("Total Price",validators=[DataRequired()]) #user
    #need_pay_supplier should be calculated
    is_used_points = BooleanField("Do you want to use your points?")
    used_points = IntegerField("How many to use?")

    #order flag
    #supplier_checked_flg = IntegerField("Supplier Checked Flag")
    #supplier_target_dt = DateField("Supplier Target Date",validators=[DataRequired()]) #supplier
    #is_remind = IntegerField("Unit Price",validators=[DataRequired()])
    #order_stat = IntegerField("Supplier Checked Flag") should be settled in code

    #comments
    user_comments = StringField("Comments")
    #supplier_comments = Column(String(500)) should be input when supplier handle this order


class UserQuoteForm(Form):
    #basic info
    quote_name = StringField("Quote Name")
    supplier_id = IntegerField("Supplier ID",validators=[DataRequired()])
    # user_id = IntegerField("User ID")
    prod_id = IntegerField("Product ID")
    prod_name = StringField("Product Name")
    prod_quantity = IntegerField("Product Quantity")
    imprint_info = StringField("Imprint Information")
    special_instruction = StringField("Special Instruction")
    lead_time = StringField("Lead Time")
    colors = StringField("Colors")
    user_perfer_unit_price = DecimalField("User Perferred Unit Price")
    user_perfer_imprinting_prices = DecimalField("User Perferred Imprinting Price")
    user_perfer_setup_cost = DecimalField("User Perferred Setup Cost")
    user_perfer_freight_cost = DecimalField("User Perferred Freight Cost")
    # user_perfer_total = DecimalField("User Perferred Total Cost")
    user_perfer_comment = StringField("User Comments")
