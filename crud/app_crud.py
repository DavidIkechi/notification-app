from sqlalchemy.orm import Session, load_only
import sys
from fastapi import HTTPException
from .crud_exception import exceptions
sys.path.append("..")
from db import models
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi_pagination import Page, Params, paginate

def create_new_client(db: Session, client_details):
    # first check if the client is already present.
    try:
        get_client = models.Client.check_single_key(db, client_details.client_key)
        if get_client is not None:
            return exceptions.client_exists_error()
        # create the client
        create_client = models.Client.create_single_client(db, 
                                                        client_details.slug, client_details.client_key)
        if create_client is None:
            return exceptions.service_error(status_code=400, detail="An error ocurred while creating client, Please try again")  
        
        db.add(create_client)
        db.commit()
        
    except Exception as e:
        return exceptions.service_error(status_code=e.status_code, detail=str(e))  

    return {
        "detail":"Client was successfully added"
    }
    
def update_client(db: Session, client_key, update_client_data):
    try:
        get_client = models.Client.check_single_key(db, client_key)
        if get_client is None:
            return exceptions.service_error(status_code=400, detail="Client with such key does not exists")   
        # update client_field
        update_client_field = models.Client.update_single_client(db, client_key, update_client_data.dict(exclude_unset=True))        
        db.commit()
        
    except Exception as e:
        return exceptions.service_error(status_code=500, detail=str(e))  

    return {
        "detail":"Client was Successfully updated"
    }
    
def update_client_key(db: Session, old_key, new_key):
    try:
        # check if the old key exists;
        get_client = models.Client.check_single_key(db, new_key.client_key)
        if get_client is not None:
            return exceptions.service_error(status_code=400, detail="Client with such key already exists")
        
        if old_key == new_key.client_key:
            return exceptions.service_error(status_code=400, detail="Old and new keys must be not be the same")
        
        return update_client(db, old_key, new_key)
           
    except Exception as e:
        return exceptions.service_error(status_code=500, detail=str(e)) 
    
def get_all_client(db: Session, page: int, page_size: int):
    try:
        
        get_all_clients = models.Client.retrieve_all_client(db)
        
        paginated_record = Params(page=page, size=page_size)
        
        return {
            "detail": paginate(get_all_clients, paginated_record)
        }
    except Exception as e:
        return exceptions.service_error(status_code=500, detail=str(e)) 

        
    
 

        

            
        
        
        
    


