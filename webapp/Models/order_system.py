from webapp.Models.db_basic import Base
from sqlalchemy import Integer, String, Column,Sequence,Boolean,DateTime,ForeignKey,DECIMAL,BIGINT
from sqlalchemy.sql import func
from datetime import datetime
from webapp.Models.user import User
from webapp.Models.prod_info import Prod_info
from webapp.Models.supplier import Supplier
from sqlalchemy.orm import relationship

class Order_system(Base):
    __tablename__= 'order_system'
    #__table_args__ = {'schema':'admin'}
    order_id = Column(Integer, primary_key = True)
    client_order_id = Column(BIGINT)
    supplier_id = Column(Integer , ForeignKey('supplier.supplier_id'))
    supplier=relationship(Supplier,backref='supp_order_sys')
    user_id = Column(Integer , ForeignKey('user.user_id'))
    user=relationship(User,backref='user_order_sys')
    prod_id = Column(Integer, ForeignKey('prod_info.prod_id'))
    prod_info=relationship(Prod_info,backref='prod_order_sys')
    prod_name = Column(String(100))
    prod_quantity=Column(Integer,default=0)
    imprint_info = Column(String(100))
    colors = Column(String(100))
    lead_time = Column(String(200))
    unit_price=Column(DECIMAL(12,2),default=0)
    imprinting_prices=Column(DECIMAL(12,2),default=0)
    setup_cost=Column(DECIMAL(12,2),default=0)
    freight_cost=Column(DECIMAL(12,2),default=0)
    total_price=Column(DECIMAL(12,2),default=0)
    need_pay_supplier=Column(DECIMAL(12,2),default=0)
    is_used_points=Column(Integer,default=0)
    used_points=Column(Integer,default=0)
    supplier_target_dt = Column(DateTime)
    user_comments = Column(String(500))
    supplier_comments = Column(String(500))
    order_stat=Column(Integer,default=0)
    valid_flg=Column(Integer,default=0)
    order_create_dt = Column(DateTime,default=func.now())
    cancel_reason = Column(String(300))
    prod_size=Column(String(100))
    special_instruction=Column(String(100))
    sys_quote_id=Column(BIGINT)


    def __repr__(self):
        return '<Order_system quote_id:%d,supplier_id:%d,user_id:%d,prod_id:%d>' % (self.quote_id,self.supplier_id,self.user_id,self.prod_id)
