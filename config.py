# This part is to define configurations for everything.
import os
from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class DatabaseConfig(BaseSettings):
    DB_HOST: str = os.getenv('DB_NOTI_HOST')
    DB_NAME: str = os.getenv('DB_NOTI_NAME')
    DB_USER: str = os.getenv('DB_NOTI_USER')
    DB_PASS: str = os.getenv('DB_NOTI_PASSWORD')
    DB_CONNECTION: str = DB_USER+":"+DB_PASS+"@"+DB_HOST+"/"+DB_NAME
    
    if os.getenv('DB_TEST'):
        DATABASE_URL: str = "sqlite:///./notification_app.db"
    else:
        DATABASE_URL: str = "mysql+mysqlconnector://"+DB_CONNECTION
    
    class Config:
        env_file = ".env"
    

dataConfig = DatabaseConfig()
    
    