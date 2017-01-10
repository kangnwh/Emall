from webapp.Models.db_basic import Base
from sqlalchemy import Integer, String, Column,Sequence,Boolean,DateTime,ForeignKey,DECIMAL
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from webapp.Models.prod_sub_cat import Prod_sub_cat
from webapp.Models.supplier import Supplier
from datetime import datetime

class V_hot_prods(Base):
    __tablename__= 'v_hot_prods'
    #__table_args__ = {'schema':'admin'}
    prod_id = Column(Integer, primary_key = True)
    prod_name = Column(String(100))
    prod_desc = Column(String(500))
    lead_time = Column(String(200))
    prod_size = Column(String(100))
    imprint_size = Column(String(100))
    price_basis = Column(String(200))
    prod_cat_sub_id = Column(Integer,ForeignKey('prod_sub_cat.prod_cat_sub_id'))
    prod_sub_cat = relationship(Prod_sub_cat)
    valid_flg=Column(Integer,default=0)
    approve_stat=Column(Integer,default=0)
    is_special_price_flg=Column(Integer,default=0)
    special_price_old=Column(DECIMAL(12,2),default=0)
    special_price_new=Column(DECIMAL(12,2),default=0)
    special_price_campaign_time= Column(DateTime,default=func.now())
    is_clearance=Column(Integer,default=0)
    is_new_prod=Column(Integer,default=0)
    is_patent_prod=Column(Integer,default=0)
    is_hot_prod=Column(Integer,default=0)
    is_del_flg=Column(Integer,default=0)
    supplier_id= Column(Integer,ForeignKey('supplier.supplier_id'))
    supplier = relationship(Supplier)
    prod_create_ts = Column(DateTime,default=func.now())
    colors = Column(String(100))
    cover_img = Column(String(200),default='default.png')
    reject_reason = Column(String(500))

    def __repr__(self):
        return '<v_hot_prods prod_id:%d,prod_name:%s>' % (self.prod_id,self.prod_name)