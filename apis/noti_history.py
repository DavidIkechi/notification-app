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

noti_history_router = APIRouter(
    prefix="/notification_history",
    tags=["Notification History"],
)

# define the required endpoints.
@noti_history_router.get('/single/{noti_hist_id}', summary="View Single Notification History", status_code=200, dependencies=[Depends(validate_client_key)])
async def view_single_history(request: Request, noti_hist_id: int, db: Session = Depends(get_db)):
    client_id = request.state.data
    
    return app_crud.get_single_history(db, client_id, noti_hist_id)

@noti_history_router.patch('/resend/{noti_hist_id}', summary="View Single Notification History", status_code=200, dependencies=[Depends(validate_client_key)])
async def resend_notification(request: Request, noti_hist_id: int, db: Session = Depends(get_db)):
    client_id = request.state.data
    
    return app_crud.resend_notification(db, client_id, noti_hist_id)

@noti_history_router.get('/', summary="Get all Notification History", status_code=200, dependencies=[Depends(validate_client_key)])
async def get_all_client(request: Request, trans_type: str = Query(default=None), page: int = Query(1, ge=1), page_size: int = 10,
                         db: Session=Depends(get_db)):
    client_id = request.state.data
    return app_crud.get_all_histories(db, page, page_size, trans_type, client_id)