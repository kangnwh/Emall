from webapp.Models.db_basic import Base
from sqlalchemy import Integer, String, Column,Sequence,Boolean,DateTime,ForeignKey
from sqlalchemy.sql import func
from webapp.Models.user import User
from sqlalchemy.orm import relationship
from datetime import datetime


class User_feedback(Base):
    __tablename__= 'user_feedback'
    #__table_args__ = {'schema':'admin'}
    feedback_id = Column(Integer, primary_key = True)
    valid_flg=Column(Integer,default=0)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    user = relationship(User,backref='in_user_feedback')
    email=Column(String(50))
    user_name = Column(String(100))
    user_comment = Column(String(3000))
    user_comment_ts = Column(DateTime,default=func.now())

    def __repr__(self):
        return '<user_feedback feedback_id:%d,user_comment:%s>' % (self.feedback_id,self.user_comment)