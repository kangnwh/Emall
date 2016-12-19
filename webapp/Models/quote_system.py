from webapp.Models.db_basic import Base
from sqlalchemy import Integer, String, Column,Sequence,Boolean,DateTime,ForeignKey,DECIMAL
from sqlalchemy.sql import func
from datetime import datetime
from webapp.Models.user import User
from webapp.Models.prod_info import Prod_info
from webapp.Models.supplier import Supplier
from sqlalchemy.orm import relationship

class Quote_system(Base):
    __tablename__= 'quote_system'
    #__table_args__ = {'schema':'admin'}
    quote_id = Column(Integer, primary_key = True)
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
    supplier_perfer_unit_price=Column(DECIMAL(12,2),default=0)
    supplier_perfer_imprinting_prices=Column(DECIMAL(12,2),default=0)
    supplier_perfer_setup_cost=Column(DECIMAL(12,2),default=0)
    supplier_perfer_freight_cost=Column(DECIMAL(12,2),default=0)
    supplier_perfer_total=Column(DECIMAL(12,2),default=0)
    supplier_perfer_comment = Column(String(300))
    user_last_quote_time = Column(DateTime)
    supplier_last_quote_time = Column(DateTime)
    valid_flg=Column(Integer,default=0)
    quote_create_time = Column(DateTime,default=func.now())


    def __repr__(self):
        return '<Quote_system quote_id:%d,supplier_id:%d,user_id:%d,prod_id:%d>' % (self.quote_id,self.supplier_id,self.user_id,self.prod_id)
