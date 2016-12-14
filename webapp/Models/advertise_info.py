from webapp.Models.db_basic import Base
from sqlalchemy import Integer, String, Column,Sequence,Boolean,DateTime,ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from webapp.Models.prod_info import Prod_info
from datetime import datetime

class Advertise_info(Base):
    __tablename__= 'advertise_info'
    #__table_args__ = {'schema':'admin'}
    adv_id = Column(Integer, primary_key = True)
    prod_id = Column(Integer,ForeignKey('prod_info.prod_id'))
    prod_info=relationship(Prod_info,backref='in_prod_info')
    valid_flg=Column(Integer,default=0)
    adv_create_ts = Column(DateTime,default=func.now())

    def __repr__(self):
        return '<advertise_info adv_id:%d,prod_id:%s>' % (self.adv_id,self.prod_id)