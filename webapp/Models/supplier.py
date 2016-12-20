from webapp.Models.db_basic import Base
from sqlalchemy import Integer, String, Column,Sequence,Boolean,DateTime
from sqlalchemy.sql import func
from datetime import datetime

from flask_login import AnonymousUserMixin

class Supplier(Base):
    __tablename__= 'supplier'
    #__table_args__ = {'schema':'admin'}
    supplier_id = Column(Integer, primary_key = True)
    supplier_name = Column(String(100), unique = True)
    password = Column(String(50))
    email = Column(String(50), unique = True)
    address = Column(String(300))
    valid_flg=Column(Integer,default=0)
    supplier_points = Column(Integer,default = 0)
    supplier_create_ts = Column(DateTime,default=func.now())


    def __repr__(self):
        return '<Supplier supplier_id:%d,supplier_name:%s>' % (self.supplier_id,self.supplier_name)

    @property
    def is_authenticated(self):
        return self.valid_flg==1
    @property
    def is_active(self):
        return self.valid_flg==1

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.supplier_id

class AnonymousSupplier(AnonymousUserMixin):
    is_authenticated = False
    is_active = False

    def get_id(self):
        return None
