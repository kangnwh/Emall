from flask_wtf import Form

from wtforms import StringField,BooleanField,IntegerField,SelectField,DecimalField,\
    FileField,DateField,DateTimeField
from wtforms.validators import DataRequired, ValidationError
from webapp.Models.db_basic import Session
from webapp.Models.prod_cat import Prod_cat
from webapp.Models.prod_sub_cat import Prod_sub_cat
from webapp.Models.prod_info import Prod_info

# def prodname_exists_check(self,field):
#         session = Session()
#         if not session.query(Prod_info).filter_by(prod_name=field.data).first() is None:
#             raise ValidationError( 'Production %s is already exists !' % field.data )

class ProductionBase(Form):

    prod_name = StringField('Production Name', validators = [DataRequired()])
    prod_desc = StringField('Production Description', validators = [DataRequired()])
    lead_time = StringField('Lead Time')
    prod_size = StringField('Production Size')
    imprint_size = StringField('Imprint Size')
    price_basis = StringField('Price Basis')
    valid_flg = BooleanField('Valid Flag', validators = [DataRequired()])
    prod_cat_sub_id = SelectField('Subcategory',choices=[],coerce=int)
    colors = StringField('Colors')
    is_special_price_flg = BooleanField('Is Special Price?')
    special_price_old = DecimalField("Original Price")
    special_price_new = DecimalField("New Price")
    special_price_campaign_time = DateField("Campaign Begin Time",format='%Y-%m-%d')
    is_clearance = BooleanField("Is Clearance ?")
    is_new_prod = BooleanField("Is New Production?")
    is_patent_prod = BooleanField("Is Patent Production?")


    #Price range
    quantity_from1 = DecimalField('Quantity From 1')
    quantity_to1 = DecimalField('Quantity To 1')
    unit_price1 = DecimalField('Unit Price 1')
    imprinting_prices1 = DecimalField('Imprinting Price 1')
    setup_cost1 = DecimalField('Setup Cost 1')
    freight_cost1 = DecimalField('Freight Cost 1')

    quantity_from2 = DecimalField('Quantity From 2')
    quantity_to2 = DecimalField('Quantity To 2')
    unit_price2 = DecimalField('Unit Price 2')
    imprinting_prices2 = DecimalField('Imprinting Price 2')
    setup_cost2 = DecimalField('Setup Cost 2')
    freight_cost2 = DecimalField('Freight Cost 2')

    quantity_from3 = DecimalField('Quantity From 3')
    quantity_to3 = DecimalField('Quantity To 3')
    unit_price3 = DecimalField('Unit Price 3')
    imprinting_prices3 = DecimalField('Imprinting Price 3')
    setup_cost3 = DecimalField('Setup Cost 3')
    freight_cost3 = DecimalField('Freight Cost 3')

    quantity_from4 = DecimalField('Quantity From 4')
    quantity_to4 = DecimalField('Quantity To 4')
    unit_price4 = DecimalField('Unit Price 4')
    imprinting_prices4 = DecimalField('Imprinting Price 4')
    setup_cost4 = DecimalField('Setup Cost 4')
    freight_cost4 = DecimalField('Freight Cost 4')

    quantity_from5 = DecimalField('Quantity From 5')
    quantity_to5 = DecimalField('Quantity To 5')
    unit_price5 = DecimalField('Unit Price 5')
    imprinting_prices5 = DecimalField('Imprinting Price 5')
    setup_cost5 = DecimalField('Setup Cost 5')
    freight_cost5 = DecimalField('Freight Cost 5')

    #Pictures
    cover_img_file = FileField('Upload Cover Picture',[DataRequired()])



class AddNewProduction(ProductionBase):
    pass

class DeleteProduction(Form):
    prod_id = IntegerField('prod id',validators = [DataRequired()])

class UpdateProduction(ProductionBase):
    prod_id = IntegerField('Prod id',validators = [DataRequired()])
    valid_flg = BooleanField('Valid Flag')

    cover_img_file = FileField('Upload Cover Picture')



class CreateNewProfitRateForm(Form):
    valid_flg=BooleanField('Is Valid', default = False)
    profit_rate=DecimalField('Profit Rate', validators = [DataRequired()])


class UpdateProfitRateForm(Form):
    profit_id = StringField("Profit ID", validators = [DataRequired()])
    valid_flg=BooleanField('Is Valid', default = False)
    profit_rate=DecimalField('Profit Rate', validators = [DataRequired()])

class DeleteProfitRateForm(Form):
    profit_id = IntegerField('ProfitId', validators = [DataRequired()])
