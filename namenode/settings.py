import sqlalchemy as sql
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_engine = create_engine('sqlite:///gudrock.db', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=db_engine)
session = Session()