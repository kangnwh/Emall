from webapp.Models.db_basic import Base
from sqlalchemy import Integer, String, Column,Sequence,Boolean,DateTime,DECIMAL
from sqlalchemy.sql import func
from datetime import datetime

from flask_login import AnonymousUserMixin

class User_reward_ref(Base):
    __tablename__= 'user_reward_ref'
    #__table_args__ = {'schema':'admin'}
    reward_ref_id = Column(Integer, primary_key = True)
    reward_rate=Column(DECIMAL(5,2),default=0)
    reward_desc = Column(String(200))
    user_reward_create_ts = Column(DateTime,default=func.now())


    def __repr__(self):
        return '<User_reward_ref reward_ref_id:%d>' % (self.reward_ref_id)
