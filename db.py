from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///model_entries_database.sqlite?check_same_thread=False')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()