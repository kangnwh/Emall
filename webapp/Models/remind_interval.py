from webapp.Models.db_basic import Base
from sqlalchemy import Integer, String, Column,Sequence,Boolean,DateTime,ForeignKey
from sqlalchemy.sql import func
from datetime import datetime
from webapp.Models.user import User
from webapp.Models.prod_info import Prod_info
from webapp.Models.supplier import Supplier
from sqlalchemy.orm import relationship
from flask_login import AnonymousUserMixin

class Remind_interval(Base):
    __tablename__= 'remind_interval'
    #__table_args__ = {'schema':'admin'}
    remind_interval=Column(Integer,default=0)

    def __repr__(self):
        return '<Remind_interval remind_interval:%d>' % (self.remind_interval)
