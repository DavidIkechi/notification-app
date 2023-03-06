# connection code here for both test and production.
from sqlalchemy import create_engine
import os
import sys
from dotenv import load_dotenv
from sqlalchemy.pool import StaticPool

load_dotenv()

if os.environ['TESTING']:
    DATABASE_URL = "sqlite:///./.db"
    engine = create_engine(DATABASE_URL, poolclass=StaticPool,
                           connect_args={"check_same_thread": False})
else:
    DB_HOST = os.environ['DB_NOTI_HOST']
    DB_NAME = os.environ['DB_NOTI_NAME']
    DB_USER = os.environ['DB_NOTI_USER']
    DB_PASS = os.environ['DB_NOTI_PASSWORD']
    DB_CONNECTION: str = DB_USER+":"+DB_PASS+"@"+DB_HOST+"/"+DB_NAME
    DATABASE_URL: str = "mysql+mysqlconnector://"+DB_CONNECTION
    engine = create_engine(dataConfig.DATABASE_URL, 
                       pool_pre_ping = True)

def get_engine():
    return engine