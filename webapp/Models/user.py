from webapp.Models.db_basic import Base
from sqlalchemy import Integer, String, Column,Sequence,Boolean,DateTime
from sqlalchemy.sql import func
from datetime import datetime

from flask_login import AnonymousUserMixin

class User(Base):
    __tablename__= 'user'
    #__table_args__ = {'schema':'admin'}
    user_id = Column(Integer, primary_key = True)
    user_name = Column(String(100), unique = True)
    password = Column(String(50))
    email = Column(String(50), unique = True)
    valid_flg=Column(Integer,default=0)
    is_admin = Column(Integer,default = 0)
    logo_link=Column(String(200),default='default_logo.png')
    is_paid = Column(Integer,default = 0)
    credit_points = Column(Integer,default = 0)
    user_create_ts = Column(DateTime,default=func.now())


    def __repr__(self):
        return '<User user_id:%d,user_name:%s>' % (self.user_id,self.user_name)

    @property
    def is_authenticated(self):
        return self.valid_flg==1
    @property
    def is_active(self):
        return self.valid_flg

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.user_id
    @property
    def is_administrator(self):
        return self.is_admin==1

    @property
    def is_member_paid(self):
        return self.is_paid==1

class AnonymousUser(AnonymousUserMixin):
    logo_link='default_logo.png'
    is_authenticated = False
    is_active = False
    is_administrator = False

    def get_id(self):
        return None
