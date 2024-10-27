from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.database.config import database_settings


SQLALCHEMY_DATABASE_URL = str(database_settings.DATABASE_URL)


engine = create_engine(SQLALCHEMY_DATABASE_URL)


Session = sessionmaker(bind=engine)


Base = declarative_base()


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()