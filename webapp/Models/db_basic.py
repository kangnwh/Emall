from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine,MetaData
from sqlalchemy.orm import sessionmaker
from webapp.config.config import META_DB


Base = declarative_base()

if META_DB.get('DB_TYPE') != 'sqlite' :
    connect_str = '{db_type}://{db_user}:{db_password}@{db_ip}:{db_port}/{db_name}?charset=utf8'.format(
        db_type = META_DB.get('DB_TYPE'),
        db_user = META_DB.get('DB_USER'),
        db_password = META_DB.get('DB_PASSWORD'),
        db_ip = META_DB.get('DB_HOST'),
        db_port = META_DB.get('DB_PORT'),
        db_name = META_DB.get('DB_NAME'),
    )
else :
    import webapp as w
    import os
    db_folder = os.path.dirname(w.__file__)
    connect_str = 'sqlite:///{db_folder}//{db_name}.db'.format(db_folder=db_folder,db_name=META_DB.get('DB_NAME'))

engine = create_engine(connect_str,pool_size=15)
metadata = MetaData(bind=engine)
Session = sessionmaker(bind=engine)


