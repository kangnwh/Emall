from flask import current_app,render_template
from webapp.Models.db_basic import Base
from sqlalchemy import Integer, String, Column,Sequence,Boolean,DateTime,ForeignKey,DECIMAL,BIGINT
from sqlalchemy.sql import func
from datetime import datetime
from webapp.Models.user import User
from webapp.Models.prod_info import Prod_info
from webapp.Models.supplier import Supplier
from sqlalchemy.orm import relationship

class Quote_system(Base):
    __tablename__= 'quote_system'
    #__table_args__ = {'schema':'admin'}
    quote_id = Column(BIGINT, primary_key = True)
    quote_name = Column(String(300))
    supplier_id = Column(Integer , ForeignKey('supplier.supplier_id'))
    supplier=relationship(Supplier,backref='supp_quote_sys')
    user_id = Column(Integer , ForeignKey('user.user_id'))
    user=relationship(User,backref='user_quote_sys')
    prod_id = Column(Integer, ForeignKey('prod_info.prod_id'))
    prod_info=relationship(Prod_info,backref='prod_quote_sys')
    prod_name = Column(String(100))
    prod_quantity=Column(Integer,default=0)
    imprint_info = Column(String(100))
    special_instruction = Column(String(100))
    lead_time = Column(String(200))
    colors = Column(String(100))
    user_perfer_unit_price=Column(DECIMAL(12,2),default=0)
    user_perfer_imprinting_prices=Column(DECIMAL(12,2),default=0)
    user_perfer_setup_cost=Column(DECIMAL(12,2),default=0)
    user_perfer_freight_cost=Column(DECIMAL(12,2),default=0)
    user_perfer_total=Column(DECIMAL(12,2),default=0)
    user_perfer_comment = Column(String(300))
    supplier_perfer_unit_price=Column(DECIMAL(12,4),default=0)
    supplier_perfer_imprinting_prices=Column(DECIMAL(12,2),default=0)
    supplier_perfer_setup_cost=Column(DECIMAL(12,2),default=0)
    supplier_perfer_freight_cost=Column(DECIMAL(12,2),default=0)
    supplier_perfer_total=Column(DECIMAL(12,2),default=0)
    supplier_perfer_comment = Column(String(300),default='')
    user_last_quote_time = Column(DateTime,default=func.now())
    supplier_last_quote_time = Column(DateTime)
    is_return_flg=Column(Integer,default=0)
    valid_flg=Column(Integer,default=0)
    quote_create_time = Column(DateTime,default=func.now())
    prod_size=Column(String(100))


    def __repr__(self):
        return '<Quote_system quote_id:%d,supplier_id:%d,user_id:%d,prod_id:%d>' % (self.quote_id,self.supplier_id,self.user_id,self.prod_id)

    def notification_to_supplier(self):
        # notification = '''<h3>Quote for Production {prod_name}</h3>
        # <h4>Quantity : {prod_quantity}</h4>
        # <h4>special_instruction : {special_instruction}</h4>
        # <a href="{host}/order/show_one_quote?quote_id={quote_id}">Click here for more detail</a>
        #
        # '''.format(prod_name=self.prod_name,
        #            prod_quantity=self.prod_quantity,
        #            special_instruction=self.special_instruction,
        #            quote_id=self.quote_id,
        #            host=current_app.config.get("SUPPLIER_APPLICATION_ADDRESS"))
        return render_template('order_temp/quote_email_notification.html',
                               this_quote=self,
                               link = "{host}/order/show_one_quote?quote_id={quote_id}".format(host=current_app.config.get("SUPPLIER_APPLICATION_ADDRESS"),quote_id=self.quote_id) )

    def notification_to_user(self):
        return render_template('order_temp/quote_email_notification.html',
                               this_quote=self,
                               link = "{host}/order/show_one_quote?quote_id={quote_id}".format(host=current_app.config.get("EMALL_APPLICATION_ADDRESS"),quote_id=self.quote_id) )