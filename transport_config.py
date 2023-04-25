from fastapi import (BackgroundTasks, UploadFile,File, Form, Depends, HTTPException, status)
from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from typing import List, Dict, Any
from jose import jwt, JWTError
from fastapi.exceptions import HTTPException
from datetime import datetime, timedelta
from jwt import credentials_exception
# from dotenv import dotenv_values
# from models import User
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastapi.responses import JSONResponse
from crud import get_user_by_email
from sqlalchemy.orm import Session
# from dotenv import load_dotenv
import os
from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr, BaseModel

def email_configuration(email_type, email_data):
    conf = ()
    if email_type.lower() == "smtp-email":
        conf = ConnectionConfig(
            MAIL_USERNAME = os.getenv('EMAIL'),
            MAIL_PASSWORD = os.getenv('PASS'),
            MAIL_FROM = os.getenv('EMAIL'),
            MAIL_PORT = 465,
            MAIL_SERVER = 'smtp.gmail.com',
            MAIL_FROM_NAME="Heed",
            MAIL_STARTTLS = False,
            USE_CREDENTIALS = True,
            MAIL_SSL_TLS= True,
            VALIDATE_CERTS = True,
            TEMPLATE_FOLDER='./templates'
        )
    
    return conf 



