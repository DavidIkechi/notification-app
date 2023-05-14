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
    NotificationType
)

from crud import app_crud
from db import models
from typing import Optional
from auth import validate_client_key
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

trans_type_router = APIRouter(
    prefix="/transport_method",
    tags=["Transport Method"],
)

@trans_type_router.get('/', summary="Get all Transport Method", status_code=200, dependencies=[Depends(validate_client_key)])
async def get_all_client(request: Request, trans_type: str = Query(default=None), page: int = Query(1, ge=1), page_size: int = 10,
                         db: Session=Depends(get_db)):
    client_id = request.state.data
    return app_crud.get_all_methods(db, page, page_size, trans_type, client_id)

@trans_type_router.get('/parameters/{trans_method}', summary="Get transport method parameter", status_code=200, dependencies=[Depends(validate_client_key)])
async def get_method_param(request: Request, trans_method: str, db: Session=Depends(get_db)):
    client_id = request.state.data
    return app_crud.get_method_parameter(db, client_id, trans_method)

  

