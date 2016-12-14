from webapp.Models.db_basic import Base
from sqlalchemy import Integer, ForeignKey, Column,Sequence,DateTime
from sqlalchemy.orm import relationship
from webapp.Models.user import User
from webapp.Models.tag import Tag

class Map_User_Tag(Base):
    __tablename__= 'Map_User_Tag'
    #__table_args__ = {'schema':'admin'}
    id = Column(Integer,Sequence('user_id_seq'), primary_key = True)

  #  user_id = Column(Integer, ForeignKey('user.id'))
  #  user = relationship(User,backref='in_tags')

    tag_id = Column(Integer, ForeignKey('tag.id'))
    tag =  relationship(Tag,backref='has_users')

    create_ts = Column(DateTime,Column.server_default)
    update_ts = Column(DateTime,Column.server_default)

    def __repr__(self):
        return '<Map_User_Tag user_id:%d,tag_id:%d>' % (self.user_id,self.tag_id)