from webapp.Models.db_basic import Base
from sqlalchemy import Integer, String, Column, Sequence, Boolean, DateTime, ForeignKey, DECIMAL
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from webapp.Models.prod_info import Prod_info
from datetime import datetime


class V_Prod_price_range(Base):
    __tablename__ = 'v_prod_price_range'
    # __table_args__ = {'schema':'admin'}
    prod_price_range_id = Column(Integer, primary_key=True)
    prod_id = Column(Integer, ForeignKey('prod_info.prod_id'))
    prod_info = relationship(Prod_info, backref='v_price_ranges')
    quantity_from1 = Column(Integer, default=1)
    quantity_to1 = Column(Integer, default=99999999)
    unit_price1 = Column(DECIMAL(12, 2), default=0)
    imprinting_prices1 = Column(DECIMAL(12, 2), default=0)
    setup_cost1 = Column(DECIMAL(12, 2), default=0)
    freight_cost1 = Column(DECIMAL(12, 2), default=0)

    quantity_from2 = Column(Integer, default=0)
    quantity_to2 = Column(Integer, default=0)
    unit_price2 = Column(DECIMAL(12, 2), default=0)
    imprinting_prices2 = Column(DECIMAL(12, 2), default=0)
    setup_cost2 = Column(DECIMAL(12, 2), default=0)
    freight_cost2 = Column(DECIMAL(12, 2), default=0)

    quantity_from3 = Column(Integer, default=0)
    quantity_to3 = Column(Integer, default=0)
    unit_price3 = Column(DECIMAL(12, 2), default=0)
    imprinting_prices3 = Column(DECIMAL(12, 2), default=0)
    setup_cost3 = Column(DECIMAL(12, 2), default=0)
    freight_cost3 = Column(DECIMAL(12, 2), default=0)

    quantity_from4 = Column(Integer, default=0)
    quantity_to4 = Column(Integer, default=0)
    unit_price4 = Column(DECIMAL(12, 2), default=0)
    imprinting_prices4 = Column(DECIMAL(12, 2), default=0)
    setup_cost4 = Column(DECIMAL(12, 2), default=0)
    freight_cost4 = Column(DECIMAL(12, 2), default=0)

    quantity_from5 = Column(Integer, default=0)
    quantity_to5 = Column(Integer, default=0)
    unit_price5 = Column(DECIMAL(12, 2), default=0)
    imprinting_prices5 = Column(DECIMAL(12, 2), default=0)
    setup_cost5 = Column(DECIMAL(12, 2), default=0)
    freight_cost5 = Column(DECIMAL(12, 2), default=0)

    prod_price_range_create_ts = Column(DateTime, default=func.now())

    def __repr__(self):
        return '<v_prod_price_range prod_price_range_id:%d,prod_id:%s>' % (self.prod_price_range_id, self.prod_id)

    def to_json(self):
        jsondata = ["["]
        # if self.quantity_to1 >0 :
        # if self.prod_info.is_special_price_flg == 1:
        #     pass
        jsondata.append(("{quantity_from:%f,") % self.quantity_from1)
        jsondata.append(("quantity_to:%f,") % self.quantity_to1)
        jsondata.append(("unit_price:%f,") % self.unit_price1)
        jsondata.append(("imprinting_prices:%f,") % self.imprinting_prices1)
        jsondata.append(("setup_cost:%f,") % self.setup_cost1)
        jsondata.append(("freight_cost:%f},") % self.freight_cost1)

        if self.quantity_to2 > 0:
            jsondata.append(("{quantity_from:%f,") % self.quantity_from2)
            jsondata.append(("quantity_to:%f,") % self.quantity_to2)
            jsondata.append(("unit_price:%f,") % self.unit_price2)
            jsondata.append(("imprinting_prices:%f,") % self.imprinting_prices2)
            jsondata.append(("setup_cost:%f,") % self.setup_cost2)
            jsondata.append(("freight_cost:%f},") % self.freight_cost2)

        if self.quantity_to3 > 0:
            jsondata.append(("{quantity_from:%f,") % self.quantity_from3)
            jsondata.append(("quantity_to:%f,") % self.quantity_to3)
            jsondata.append(("unit_price:%f,") % self.unit_price3)
            jsondata.append(("imprinting_prices:%f,") % self.imprinting_prices3)
            jsondata.append(("setup_cost:%f,") % self.setup_cost3)
            jsondata.append(("freight_cost:%f},") % self.freight_cost3)

        if self.quantity_to4 > 0:
            jsondata.append(("{quantity_from:%f,") % self.quantity_from4)
            jsondata.append(("quantity_to:%f,") % self.quantity_to4)
            jsondata.append(("unit_price:%f,") % self.unit_price4)
            jsondata.append(("imprinting_prices:%f,") % self.imprinting_prices4)
            jsondata.append(("setup_cost:%f,") % self.setup_cost4)
            jsondata.append(("freight_cost:%f},") % self.freight_cost4)

        if self.quantity_to5 > 0:
            jsondata.append(("{quantity_from:%f,") % self.quantity_from5)
            jsondata.append(("quantity_to:%f,") % self.quantity_to5)
            jsondata.append(("unit_price:%f,") % self.unit_price5)
            jsondata.append(("imprinting_prices:%f,") % self.imprinting_prices5)
            jsondata.append(("setup_cost:%f,") % self.setup_cost5)
            jsondata.append(("freight_cost:%f}") % self.freight_cost5)

        jsondata.append("]")

        return "".join(jsondata)

    def get_prices(self, quantity):
        valid_prices=[]
        if self.quantity_to5>0:
             valid_prices.append([self.quantity_from5,self.unit_price5,self.imprinting_prices5 , self.setup_cost5 , self.freight_cost5])
        if self.quantity_to4>0:
             valid_prices.append([self.quantity_from4,self.unit_price4,self.imprinting_prices4 , self.setup_cost4 , self.freight_cost4])
        if self.quantity_to3>0:
             valid_prices.append([self.quantity_from3,self.unit_price3,self.imprinting_prices3 , self.setup_cost3 , self.freight_cost3])
        if self.quantity_to2>0:
             valid_prices.append([self.quantity_from2,self.unit_price2,self.imprinting_prices2 , self.setup_cost2 , self.freight_cost2])
        if self.quantity_to1>0:
             valid_prices.append([self.quantity_from1,self.unit_price1,self.imprinting_prices1 , self.setup_cost1 , self.freight_cost1])

        for p in valid_prices:
            if quantity>= p[0]:
                return p[1]*quantity + p[2]+p[3]+p[4],p[1],p[2],p[3],p[4]

        return 0,0,0,0,0
