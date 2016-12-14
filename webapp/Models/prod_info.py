from webapp.Models.db_basic import Base
from sqlalchemy import Integer, String, Column,Sequence,Boolean,DateTime,ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from webapp.Models.prod_sub_cat import Prod_sub_cat
from datetime import datetime

class Prod_info(Base):
    __tablename__= 'prod_info'
    #__table_args__ = {'schema':'admin'}
    prod_id = Column(Integer, primary_key = True)
    prod_name = Column(String(100))
    prod_desc = Column(String(500))
    lead_time = Column(String(200))
    prod_size = Column(String(100))
    imprint_size = Column(String(100))
    price_basis = Column(String(200))
    prod_cat_sub_id = Column(Integer,ForeignKey('prod_sub_cat.prod_cat_sub_id'))
    prod_sub_cat = relationship(Prod_sub_cat,backref='prod_info')
    valid_flg=Column(Integer,default=0)
    prod_create_ts = Column(DateTime,default=func.now())
    colors = Column(String(100))
    cover_img = Column(String(200),default='default.png')

    def __repr__(self):
        return '<prod_info prod_id:%d,prod_name:%s>' % (self.prod_id,self.prod_name)