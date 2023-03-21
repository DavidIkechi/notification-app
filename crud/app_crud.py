import sys

from fastapi import HTTPException
from sqlalchemy.orm import Session, load_only

sys.path.append("..")
from utils import *
from db import models
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi_pagination import Page, Params
from response_handler import error_response as exceptions
from response_handler import success_response
from fastapi_pagination.ext.sqlalchemy import paginate


def create_new_client(db: Session, client_details):
    # first check if the client is already present.
    try:
        get_client = models.Client.check_single_key(db, client_details.client_key)
        if get_client is not None:
            return exceptions.bad_request_error(detail="Opps!, Client already exists!")
        # create the client
        create_client = models.Client.create_single_client(db, 
                                                        client_details.slug, client_details.client_key)
        if create_client is None:
            return exceptions.bad_request_error(detail="An error ocurred while creating client, Please try again")  
        
        db.add(create_client)
        db.commit()
        
    except Exception as e:
        return exceptions.server_error(status_code=500, detail=str(e))  

    return success_response.success_message(
        status_code=201, detail="Client was successfully created")
    
def update_client(db: Session, client_id, update_client_data):
    try:
        get_client = models.Client.get_client_by_id(db, client_id)
        if get_client is None:
            return exceptions.bad_request_error(detail="Client with such id does not exists")   
        # update client_field
        update_client_field = models.Client.update_single_client(db, client_id, update_client_data.dict(exclude_unset=True))        
        if not update_client_field:
            return exceptions.bad_request_error(detail="An error ocurred while updating client, Please try again")
            
        db.add(update_client_field)
        db.commit()
        db.refresh(update_client_field)
        
    except Exception as e:
        return exceptions.server_error(status_code=500, detail=str(e))  

    return success_response.success_message(
        status_code=200, detail=update_client_field)
    
def update_client_key(db: Session, client_id, new_key):
    try:
        # check if the old key exists;
        get_client = models.Client.check_single_key(db, new_key.client_key)
        if get_client is not None:
            return exceptions.bad_request_error(detail="Client with such key already exists")
                
        return update_client(db, client_id, new_key)
           
    except Exception as e:
        return exceptions.server_error(status_code=500, detail=str(e)) 
    
def get_all_clients(db: Session, page: int, page_size: int):
    try:  
        # get the client object for the desired columns.
        client_object = models.Client.get_client_object(db).options(load_only(models.Client.slug, models.Client.status))
        # calculate page offset.
        # page_offset = get_offset(page, page_size)
        page_offset = Params(page=page, size=page_size)

        # data_result = client_object.offset(page_offset).limit(page_size).all()
        data_result = paginate(client_object, page_offset)
      
        return success_response.success_message(
            status_code=200, detail=data_result)
        
    except Exception as e:
        return exceptions.server_error(status_code=500, detail=str(e)) 

        
    
 

        

            
        
        
        
    


