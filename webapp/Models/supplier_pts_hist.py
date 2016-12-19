from webapp.Models.db_basic import Base
from sqlalchemy import Integer, String, Column,Sequence,Boolean,DateTime,ForeignKey
from sqlalchemy.sql import func
from datetime import datetime
from webapp.Models.user import User
from webapp.Models.prod_info import Prod_info
from webapp.Models.supplier import Supplier
from sqlalchemy.orm import relationship
from flask_login import AnonymousUserMixin

class Supplier_pts_hist(Base):
    __tablename__= 'supplier_pts_hist'
    #__table_args__ = {'schema':'admin'}
    supplier_pts_hist_id = Column(Integer, primary_key = True)
    supplier_id = Column(Integer , ForeignKey('supplier.supplier_id'))
    supplier=relationship(Supplier,backref='supp_pts_hist')
    before_pts=Column(Integer,default=0)
    after_pts=Column(Integer,default=0)
    update_reason = Column(String(300))
    pts_update_ts = Column(DateTime,default=func.now())

    def __repr__(self):
        return '<Supplier_pts_hist supplier_pts_hist_id:%d,supplier_id:%d>' % (self.supplier_pts_hist_id,self.supplier_id)
