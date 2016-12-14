from webapp.Models.db_basic import Base
from sqlalchemy import Integer, String, Column,Sequence,Boolean,DateTime,ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from webapp.Models.prod_cat import Prod_cat
from datetime import datetime

class Prod_sub_cat(Base):
    __tablename__= 'prod_sub_cat'
    #__table_args__ = {'schema':'admin'}
    prod_cat_sub_id = Column(Integer, primary_key = True)
    prod_cat_sub_name = Column(String(100), unique = True)
    valid_flg=Column(Integer,default=0)
    prod_cat_sub_desc = Column(String(500))

    prod_cat_id = Column(Integer, ForeignKey('prod_cat.prod_cat_id'))
    prod_cat = relationship(Prod_cat,backref='prod_sub_cat')

    prod_cat_sub_create_ts = Column(DateTime,default=func.now())

    def __repr__(self):
        return '<prod_sub_cat prod_cat_sub_id:%d,prod_cat_sub_name:%s>' % (self.prod_cat_sub_id,self.prod_cat_sub_name)

    def __cmp__(self,other):
        if self.valid_flg<other.valid_flg:
            return -1
        elif self.valid_flg==other.valid_flg:
            return 0
        else:
            return