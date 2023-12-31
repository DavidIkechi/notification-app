from fastapi import APIRouter, Depends, Request, HTTPException, Query, Path
from sqlalchemy.orm import Session
import sys, asyncio
sys.path.append("..")
from db.session import get_db
from schema import (
    NotificationDataSchema, 
    NotificationUpdateSchema,
    NotificationHistorySchema,
    NotificationDataEndpointSchema,
    NotificationType,
    TransportConfigurationSchema
)

from crud import app_crud
from db import models
from typing import Optional
from auth import validate_client_key
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

trans_config_router = APIRouter(
    prefix="/transport_configuration",
    tags=["Transport Configuration"],
)

@trans_config_router.patch('/enable/{trans_channel}', summary="Enable a Transport Configuration", status_code=200, dependencies=[Depends(validate_client_key)])
async def enable_transport(request: Request, trans_channel: str, noti_type: NotificationType, db: Session = Depends(get_db)):
    client_id = request.state.data
    trans_state = {
        'transport_state': True
    }
    
    return app_crud.update_trans_config(db, client_id, trans_channel, noti_type, trans_state)

@trans_config_router.patch('/disable/{trans_channel}', summary="Disable a Transport Configuration", status_code=200, dependencies=[Depends(validate_client_key)])
async def enable_transport(request: Request, trans_channel: str, noti_type: NotificationType, db: Session = Depends(get_db)):
    client_id = request.state.data
    trans_state = {
        'transport_state': False
    }
    
    return app_crud.update_trans_config(db, client_id, trans_channel, noti_type, trans_state)

@trans_config_router.put('/activate/{trans_channel}', summary="Activate a Transport Configuration", status_code=200, dependencies=[Depends(validate_client_key)])
async def enable_transport(request: Request, trans_channel: str, noti_type: NotificationType, db: Session = Depends(get_db)):
    client_id = request.state.data
    
    return app_crud.activate_trans_config(db, client_id, trans_channel, noti_type)

@trans_config_router.post('/create', summary="Create Transport Configuration", status_code=201, dependencies=[Depends(validate_client_key)])
async def create_configuration(request: Request, trans_schema: TransportConfigurationSchema, db: Session = Depends(get_db)):
    client_id = request.state.data
    return app_crud.create_config(db, client_id, trans_schema)

@trans_config_router.patch('/update', summary="Update Transport Configuration", status_code=200, dependencies=[Depends(validate_client_key)])
async def create_configuration(request: Request, trans_schema: TransportConfigurationSchema, db: Session = Depends(get_db)):
    client_id = request.state.data
    return app_crud.update_config(db, client_id, trans_schema)