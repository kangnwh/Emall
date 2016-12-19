from webapp.Models.db_basic import Base
from sqlalchemy import Integer, String, Column,Sequence,Boolean,DateTime,DECIMAL
from sqlalchemy.sql import func
from datetime import datetime

from flask_login import AnonymousUserMixin

class Supplier_rebate_ref(Base):
    __tablename__= 'supplier_rebate_ref'
    #__table_args__ = {'schema':'admin'}
    rebate_ref_id = Column(Integer, primary_key = True)
    supplier_points_from=Column(Integer,default=0)
    supplier_points_to=Column(Integer,default=0)
    rebate_rate=Column(DECIMAL(5,2),default=0)
    rebate_desc = Column(String(200))
    supplier_level=Column(Integer,default=0)
    supplier_rebate_create_ts = Column(DateTime,default=func.now())


    def __repr__(self):
        return '<Supplier_rebate_ref rebate_ref_id:%d>' % (self.rebate_ref_id)
