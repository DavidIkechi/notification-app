# connection code here for both test and production.
import os
import sys
from dotenv import load_dotenv

load_dotenv()
    
def get_db_conn_string():
    DB_HOST = os.environ['DB_NOTI_HOST']
    DB_NAME = os.environ['DB_NOTI_NAME']
    DB_USER = os.environ['DB_NOTI_USER']
    DB_PASS = os.environ['DB_NOTI_PASSWORD']
    DB_CONNECTION = DB_USER+":"+DB_PASS+"@"+DB_HOST+"/"+DB_NAME
    
    return "mysql+mysqlconnector://"+DB_CONNECTION