from fastapi import APIRouter, Depends, Request, HTTPException, Query, Path
from sqlalchemy.orm import Session
import sys, asyncio
sys.path.append("..")
from db.session import get_db
from crud import app_crud
from db import models
from typing import Optional
from auth import validate_client_key
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

noti_variable_router = APIRouter(
    prefix="/notification_variables",
    tags=["Notification Variables"],
)

@noti_variable_router.get("/single/{noti_type_slug}", summary="Get Single Notification Variable for Notification Type", status_code=200, dependencies=[Depends(validate_client_key)])
async def get_single_notification_variable(request: Request, noti_type_slug: str, db: Session = Depends(get_db)):
    client_id = request.state.data
    return app_crud.get_single_noti_variable(db, noti_type_slug)

