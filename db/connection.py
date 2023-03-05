# connection code here for both test and production.
from sqlalchemy import create_engine
import sys
sys.path.append("..")
from config import dataConfig

engine = create_engine(dataConfig.DATABASE_URL, pool_pre_ping = True)

def get_engine():
    return engine