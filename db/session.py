# for creating sessions
from sqlalchemy.orm import sessionmaker, declarative_base
from .connection import get_engine


db_engine = get_engine()

Session = sessionmaker(
    auto_commit=False,
    auto_flush=False,
    bind=db_engine
    ) 

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

Base = declarative_base()