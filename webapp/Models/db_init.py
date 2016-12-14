from webapp.Models.db_basic import engine,Base


def recreate_all():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)