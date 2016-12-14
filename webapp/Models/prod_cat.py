from webapp.Models.db_basic import Base
from sqlalchemy import Integer, String, Column,Sequence,Boolean,DateTime
from sqlalchemy.sql import func
from datetime import datetime

class Prod_cat(Base):
    __tablename__= 'prod_cat'
    #__table_args__ = {'schema':'admin'}
    prod_cat_id = Column(Integer, primary_key = True)
    prod_cat_name = Column(String(100), unique = True)
    valid_flg=Column(Integer,default=0)
    prod_cat_desc = Column(String(500))
    prod_cat_create_ts = Column(DateTime,default=func.now())
    prod_cat_order=Column(Integer,default=0)

    def __repr__(self):
        return '<prod_cat prod_cat_id:%d,prod_cat_name:%s>' % (self.prod_cat_id,self.prod_cat_name)