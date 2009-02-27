import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.orm import sessionmaker
import meta
import models


def init_model(db_engine):
    sm = orm.sessionmaker(autoflush=True, bind=db_engine, expire_on_commit=True, autocommit=False)
    meta.engine = db_engine
    meta.session = orm.scoped_session(sm)
    meta.metadata.create_all(bind=db_engine)
