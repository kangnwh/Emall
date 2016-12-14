from flask_wtf import Form
from wtforms import StringField,BooleanField,PasswordField,IntegerField,SelectField
from wtforms.validators import DataRequired, ValidationError
from webapp.Models.db_basic import Session
from webapp.Models.prod_cat import Prod_cat
from webapp.Models.prod_sub_cat import Prod_sub_cat


def levelone_not_exists_check(self,field):
        session = Session()
        if not session.query(Prod_cat).filter_by(prod_cat_name=field.data).first() is None:
            raise ValidationError( 'Level One Category %s is already exists !' % field.data )

def leveltwo_not_exists_check(self,field):
        session = Session()
        if not session.query(Prod_sub_cat).filter_by(prod_cat_sub_name=field.data).first() is None:
            raise ValidationError( 'Level One Category %s is already exists !' % field.data )

class DeleteLevelOneForm(Form):
    prod_cat_id = IntegerField('Level One Category ID', validators = [DataRequired()])

class CreateNewLevelOneForm(Form):
    prod_cat_name = StringField('Level One Category Name', validators = [DataRequired(),levelone_not_exists_check])
    prod_cat_desc = StringField('Level One Category Description')
    prod_cat_order = IntegerField('Level One Order Number')

class UpdateLevelOneForm(Form):
    prod_cat_id = IntegerField('Product Categroy ID',validators = [DataRequired()])
    prod_cat_name = StringField('Level One Category Name', validators = [DataRequired()])
    prod_cat_desc = StringField('Level One Category Description')
    prod_cat_order = IntegerField('Level One Order Number')
    valid_flg = BooleanField('Valid Flag')


class DeleteLevelTwoForm(Form):
    prod_cat_sub_id = IntegerField('Level One Category ID', validators = [DataRequired()])

class CreateNewLevelTwoForm(Form):
    prod_cat_sub_name = StringField('Level One Category Name', validators = [DataRequired(),levelone_not_exists_check])
    prod_cat_id = SelectField('Product Category ID',choices=[],coerce=int)#,choices=[(i.prod_cat_id,i.prod_cat_name) for i in level_one_list])
    prod_cat_sub_desc = StringField('Level One Category Description')

class UpdateLevelTwoForm(Form):

    prod_cat_sub_id = IntegerField('Product Subcategroy ID',validators = [DataRequired()])
    prod_cat_id = SelectField('Product Category ID',choices=[],coerce=int)

    prod_cat_sub_name = StringField('Level One Category Name', validators = [DataRequired()])
    prod_cat_sub_desc = StringField('Level One Category Description')
    valid_flg = BooleanField('Valid Flag')