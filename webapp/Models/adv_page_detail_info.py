from webapp.Models.db_basic import Base
from sqlalchemy import Integer, String, Column,Sequence,Boolean,DateTime,ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from webapp.Models.prod_info import Prod_info
from datetime import datetime

class Adv_page_detail_info(Base):
    __tablename__= 'adv_page_detail_info'
    #__table_args__ = {'schema':'admin'}
    adv_id = Column(Integer,primary_key=True)
    adv_level = Column(Integer)
    adv_prod_id =  Column(Integer, ForeignKey('prod_info.prod_id'))
    prod_info = relationship(Prod_info, backref='prod_adv_sys')
    adv_prod_order = Column(Integer)


    def __repr__(self):
        return '<adv_page_detail_info adv_level:%d,adv_prod_id:%d,adv_prod_order:%d>' % (self.adv_level,self.adv_prod_id,self.adv_prod_order)