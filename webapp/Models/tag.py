from webapp.Models.db_basic import Base
from sqlalchemy import Integer, ForeignKey, String, Column,Sequence,DateTime

from sqlalchemy.orm import relationship
from webapp.Models.user import User


class Tag(Base):
    __tablename__= 'tag'
    #__table_args__ = {'schema':'admin'}
    id = Column(Integer, Sequence('tag_in_sequence'),primary_key = True)
    tag_name = Column(String(64), unique = True)
 #   owner_id = Column(Integer, ForeignKey('user.id'))
 #   owner = relationship(User,backref='tag')
    description = Column(String(1024), default = '热门标签')
    create_ts = Column(DateTime,Column.server_default)

    def __repr__(self):
        return '<Tag id:%d,tag_name:%s,owner_id:%d,description:%s,owner:%s>' % (self.id,self.tag_name,self.owner_id,self.description,self.owner)