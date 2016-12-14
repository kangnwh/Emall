from webapp.Models.db_basic import Base
from sqlalchemy import Integer, String, Column,Sequence,Boolean,DateTime,ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from webapp.Models.prod_info import Prod_info
from datetime import datetime

class Prod_pic_info(Base):
    __tablename__= 'prod_pic_info'
    #__table_args__ = {'schema':'admin'}
    prod_pic_id = Column(Integer, primary_key = True)
    prod_id = Column(Integer,ForeignKey('prod_info.prod_id'))
    prod_info=relationship(Prod_info,backref='prod_pics')
    img_desc=Column(String(100))
    image_path=Column(String(100))
    valid_flg=Column(Integer,default=0)
    prod_pic_create_ts = Column(DateTime,default=func.now())

    def __repr__(self):
        return '<prod_pic_id prod_pic_id:%d,prod_id:%s>' % (self.prod_pic_id,self.prod_id)