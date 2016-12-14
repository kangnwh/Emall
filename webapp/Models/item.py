from webapp.Models.db_basic import Base
from sqlalchemy import Integer, ForeignKey, String, Column,Sequence,DateTime,UnicodeText
from sqlalchemy.orm import relationship
from webapp.Models.user import User


class Item(Base):
    __tablename__= 'item'
    #__table_args__ = {'schema':'admin'}
    id = Column(Integer, Sequence('item_in_sequence'),primary_key = True)
    title = Column(String(64), unique = True)

#    owner_id = Column(Integer, ForeignKey('user.id'))
#    owner = relationship(User,backref='item')

    content = Column(UnicodeText, default = '')

    create_ts = Column(DateTime,Column.server_default)
    update_ts = Column(DateTime,Column.server_default)

    def __repr__(self):
        return '<Tag id:%d,tag_name:%s,owner_id:%d,description:%s,owner:%s>' % (self.id,self.tag_name,self.owner_id,self.description,self.owner)