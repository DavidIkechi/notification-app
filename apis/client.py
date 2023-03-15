from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.middleware import Middleware
from sqlalchemy.orm import Session
import sys, asyncio
sys.path.append("..")
from db.session import get_db
from schema import ClientSchema, UpdateStatusSchema, UpdateClientKeySchema
from crud import app_crud
from db import models

# define the function for the middleware
async def validate_client_key(request: Request, db: Session=Depends(get_db)):
    # get the client key from the header.
    get_client_key = request.headers.get("Client-Authorization")
    # if the client key is missing throw an exception.
    if not get_client_key:
        raise HTTPException(status_code=401, detail="Client key is missing")
    # check if the client key is valid.
    get_client = models.Client.check_single_key(db, get_client_key)
    if get_client is None:
        raise HTTPException(status_code=401, detail="Client details not found")
    # client is inactive
    if get_client.status is False:
        raise HTTPException(status_code=401, detail="Inactive account")
    
    return get_client
    
# dependencies=[Depends(validate_client_key)])
#     client = request.state.client
client_router = APIRouter(
    prefix="/clients",
    tags=["clients"],
)

@client_router.post("/create_client", summary="create a single client", status_code=201)
async def create_new_client(client_details: ClientSchema, db: Session = Depends(get_db)):
    return app_crud.create_new_client(db, client_details)

@client_router.patch("/deactivate_client", summary="deactivate a client", status_code=200)
async def deactivate_client(db: Session= Depends(get_db), client: models.Client = Depends(validate_client_key)):
    # set the status to False.
    update_data = {
        "status": False
    }
    return app_crud.update_client(db, client.client_key, UpdateStatusSchema(**update_data))

@client_router.patch('/reactivate_client/{client_key}', summary="Reactivate a client", status_code=200)
async def reactivate_client(client_key: str, db: Session= Depends(get_db)):
    update_data = {
        "status": True
    }
    return app_crud.update_client(db, client_key, UpdateStatusSchema(**update_data))

@client_router.patch('/update_client_key', summary="Update single client key", status_code=200)
async def update_client_key(client_key: UpdateClientKeySchema, db: Session = Depends(get_db),
                            client: models.Client = Depends(validate_client_key)):
    
    return app_crud.update_client_key(db, client.client_key, client_key)


@client_router.get('/get_all_clients', summary="Get all clients status and slugname", status_code=200)
async def get_all_client(page: int = 1, page_size: int = 10, db: Session=Depends(get_db)):
    return app_crud.get_all_client(db, page, page_size)