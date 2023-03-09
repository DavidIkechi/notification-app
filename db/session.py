# for creating sessions
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool, NullPool
from sqlalchemy import create_engine
from .connection import get_db_conn_string
import os
from dotenv import load_dotenv

load_dotenv()

if os.environ['TESTING']:
    database_url = "sqlite://"
    poolclass = StaticPool
    pre_ping = False
    connect_args = {"check_same_thread": False}
else:
    database_url = get_db_conn_string()
    poolclass = NullPool
    pre_ping = True
    connect_args = {}
  
engine = create_engine(database_url, pool_pre_ping = pre_ping,
                       poolclass = poolclass, connect_args = connect_args)  


Session = sessionmaker(auto_commit=False, auto_flush=False, bind=engine) 

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
        
Base = declarative_base()