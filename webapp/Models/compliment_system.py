from webapp.Models.db_basic import Base
from sqlalchemy import Integer, String, Column,Sequence,Boolean,DateTime,ForeignKey,BIGINT
from sqlalchemy.sql import func
from datetime import datetime
from webapp.Models.user import User
from webapp.Models.prod_info import Prod_info
from webapp.Models.order_system import Order_system
from sqlalchemy.orm import relationship
from flask_login import AnonymousUserMixin

class Compliment_system(Base):
    __tablename__= 'compliment_system'
    #__table_args__ = {'schema':'admin'}
    compliment_id = Column(Integer, primary_key = True)
    user_id = Column(Integer , ForeignKey('user.user_id'))
    user=relationship(User,backref='user_compliment_sys')
    prod_id = Column(Integer, ForeignKey('prod_info.prod_id'))
    prod_info=relationship(Prod_info,backref='prod_compliment_sys')
    order_id = Column(BIGINT , ForeignKey('order_system.order_id'))
    order_system=relationship(Order_system,backref='order_compliment_sys')
    compliment_rate=Column(Integer,default=0)
    user_compliment_comments = Column(String(3000))
    user_compliment_time = Column(DateTime,default=func.now())


    def __repr__(self):
        return '<Compliment_system compliment_id:%d,user_id:%d,prod_id:%d>' % (self.compliment_id,self.user_id,self.prod_id)
