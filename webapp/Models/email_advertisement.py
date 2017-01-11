from webapp.Models.db_basic import Base
from sqlalchemy import Integer, String, Column, Sequence, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from webapp.Models.supplier import Supplier
from datetime import datetime


class Email_advertisement(Base):
    __tablename__ = 'email_advertisement'
    # __table_args__ = {'schema':'admin'}
    email_advertisement_id = Column(Integer, primary_key=True)
    supplier_id = Column(Integer, ForeignKey('supplier.supplier_id'))
    supplier = relationship(Supplier, backref='email_advertisement')
    title = Column(String(255))
    ad_content = Column(String(30000))
    approval_status = Column(Integer)

    submit_date = Column(DateTime, default=func.now())
    approve_date = Column(DateTime)
    email_send_date = Column(DateTime)

    def __repr__(self):
        return '<email_advertisement email_advertisement_id:%d,supplier_id:%s>' % (self.email_advertisement_id, self.supplier_id)
