from webapp.Models.db_basic import Base
from sqlalchemy import Integer, String, Column,Sequence,Boolean,DateTime,ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from webapp.Models.prod_info import Prod_info
from datetime import datetime

class Adv_page_info(Base):
    __tablename__= 'adv_page_info'
    #__table_args__ = {'schema':'admin'}
    adv_level = Column(Integer)
    adv_level_name = Column(String(200))

    def __repr__(self):
        return '<adv_page_info adv_level:%d,adv_level_name:%s>' % (self.adv_level,self.adv_level_name)