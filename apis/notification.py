from fastapi import APIRouter, Depends, Request, HTTPException, Query
from sqlalchemy.orm import Session
import sys, asyncio
sys.path.append("..")
from db.session import get_db
from schema import (
    NotificationDataSchema, 
    NotificationUpdateSchema,
    NotificationHistorySchema
)

from crud import app_crud
from db import models
from auth import validate_client_key
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

notification_router = APIRouter(
    prefix="/notification",
    tags=["notification"],
)

@notification_router.post('/create', summary="Create Notification Sample", status_code=200, dependencies=[Depends(validate_client_key)])
async def create_noti_sample(request: Request, noti_schema: NotificationDataSchema, db: Session = Depends(get_db)):
    client_id = request.state.data
    return app_crud.create_noti_sample(db, client_id, noti_schema)

@notification_router.patch('/enable/{noti_id}', summary="Enable Notification Sample", status_code=200, dependencies=[Depends(validate_client_key)])
async def enable_noti_sample(request: Request, noti_id: int, db: Session = Depends(get_db)):
    client_id = request.state.data
    noti_state = {
        'notification_state': True
    }
    
    return app_crud.update_noti_sample(db, client_id, noti_id, NotificationUpdateSchema(**noti_state))

@notification_router.patch('/disable/{noti_id}', summary="Disable Notification Sample", status_code=200, dependencies=[Depends(validate_client_key)])
async def disable_noti_sample(request: Request, noti_id: int, db: Session = Depends(get_db)):
    client_id = request.state.data
    noti_state = {
        'notification_state': False
    }
    
    return app_crud.update_noti_sample(db, client_id, noti_id, NotificationUpdateSchema(**noti_state))
    
@notification_router.patch('/update/{noti_id}', summary="Update Notification Sample", status_code=200, dependencies=[Depends(validate_client_key)])
async def update_noti_sample(request: Request, noti_id: int, noti_schema: NotificationUpdateSchema, db: Session = Depends(get_db)):
    client_id = request.state.data
    return app_crud.update_noti_sample(db, client_id, noti_id, noti_schema)

@notification_router.post('/send/{noti_id}', summary="Send Notification", status_code=200, dependencies=[Depends(validate_client_key)])
async def send_notification(request: Request, noti_id: int, sche_variables: NotificationHistorySchema, db: Session = Depends(get_db)):
    client_id = request.state.data
    return app_crud.send_notification(db, client_id, noti_id, sche_variables)

