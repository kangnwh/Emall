from webapp.Models.db_basic import Base
from sqlalchemy import Integer, ForeignKey, Column,Sequence,DateTime
from sqlalchemy.orm import relationship
from webapp.Models import user,Tag,Item

class Map_Tag_Item(Base):
    __tablename__= 'map_tag_item'
    #__table_args__ = {'schema':'admin'}
    id = Column(Integer,Sequence('map_tag_item_id_seq'), primary_key = True)

    tag_id = Column(Integer, ForeignKey('tag.id'))
    tag =  relationship(Tag,backref='has_items')

    item_id = Column(Integer, ForeignKey('item.id'))
    item = relationship(Tag,backref='with_tags')

    create_ts = Column(DateTime,Column.server_default)
    update_ts = Column(DateTime,Column.server_default)


    def __repr__(self):
        return '<Map_Tag_Item tag_id:%d,tag:%s,item_id:%d,item:%s>' % (self.tag_id,self.tag,self.item_id,self.item)