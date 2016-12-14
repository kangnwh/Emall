from webapp.Models.db_basic import Base
from sqlalchemy import Integer, String, Column,Sequence,Boolean,DateTime,DECIMAL
from sqlalchemy.sql import func
from datetime import datetime


class Prod_profit_rate(Base):
    __tablename__= 'prod_profit_rate'
    #__table_args__ = {'schema':'admin'}
    profit_id = Column(Integer, primary_key = True)
    valid_flg=Column(Integer,default=0)
    profit_rate=Column(DECIMAL(4,2),default=0)

    profit_rate_create_ts = Column(DateTime,default=func.now())

    def __repr__(self):
        return '<prod_profit_rate profit_id:%d,profit_rate:%s>' % (self.profit_id,self.profit_rate)