import sys

from fastapi import HTTPException
# from sqlalchemy.orm import Session, load_only

sys.path.append("..")
from utils import *
from db import models
from db.session import Session
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi_pagination import Page, Params
from response_handler import error_response as exceptions
from response_handler import success_response
from fastapi_pagination.ext.sqlalchemy import paginate


db = Session()


def create_new_client(db, client_details):
    # first check if the client is already present.
    try:
        get_client = models.Client.check_single_key(db, client_details.client_key)
        if get_client is not None:
            return exceptions.bad_request_error("Opps!, Client already exists!")
        # create the client
        create_client = models.Client.create_single_client(db, 
                                                        client_details.slug, client_details.client_key)
        if create_client is None:
            return exceptions.bad_request_error("An error ocurred while creating client, Please try again")  
        
        db.add(create_client)
        db.commit()
        
    except Exception as e:
        return exceptions.server_error(detail=str(e))  

    return success_response.success_message([], "Client was successfully created", 201)
    
def update_client(db, client_id, update_client_data):
    try:
        get_client = models.Client.get_client_by_id(db, client_id)
        if get_client is None:
            return exceptions.bad_request_error("Client with such id does not exists")   
        # update client_field
        update_client_field = models.Client.update_single_client(db, client_id, update_client_data.dict(exclude_unset=True))        
        if not update_client_field:
            return exceptions.bad_request_error("An error ocurred while updating client, Please try again")
            
        db.add(update_client_field)
        db.commit()
        db.refresh(update_client_field)
        
    except Exception as e:
        return exceptions.server_error(detail=str(e))  

    return success_response.success_message(update_client_field, "Client record was successfully updated")
    
def update_client_key(db, client_id, new_key):
    try:
        # check if the old key exists;
        get_client = models.Client.check_single_key(db, new_key.client_key)
        if get_client is not None:
            return exceptions.bad_request_error("Client with such key already exists")
                
        return update_client(db, client_id, new_key)
           
    except Exception as e:
        return exceptions.server_error(str(e)) 
    
def get_all_clients(db, page: int, page_size: int):
    try:  
        # get the client object for the desired columns.
        client_object = models.Client.get_client_object(db)
        # calculate page offset.
        # page_offset = get_offset(page, page_size)
        page_offset = Params(page=page, size=page_size)

        # data_result = client_object.offset(page_offset).limit(page_size).all()
        data_result = paginate(client_object, page_offset)
      
        return success_response.success_message(data_result)
        
    except Exception as e:
        return exceptions.server_error(str(e))
    
    
def create_noti_sample(db, client_id, noti_schema):
    try:
        # first check if the client_id matches with id passed.
        if client_id != noti_schema.client_id:
            return exceptions.bad_request_error("Client ID doesn't match with Authorization ID")
        # check if the notification sample for that client and channel exists.
        check_noti = models.NotificationSample.check_noti_sample_by_noti_type_tran(
            db, client_id, noti_schema.noti_type_id, noti_schema.trans_channel_id)
        
        if check_noti is not None:
            return exceptions.bad_request_error("Notification Sample for Notification Type already exists!")
        # create the Notification sample.
        noti_sample = models.NotificationSample.create_noti_sample(db, noti_schema.dict(exclude_unset=True, exclude_none=True))
        db.add(noti_sample)
        db.commit()

    except Exception as e:
        return exceptions.server_error(str(e))

    return success_response.success_message([], "Notification Sample was successfully created!", 201)
    
def update_noti_sample(db, client_id: int, noti_id: int, update_noti_data):
    try:
        # check if the noti matches the client.
        check_noti = models.NotificationSample.get_noti_sample_by_id(db, noti_id)
        if check_noti is None:
            return exceptions.bad_request_error("Notification with such ID doesn't exists")
        
        if check_noti.client_id != client_id:
            return exceptions.bad_request_error("Client ID is not associated with Notification Sample type")
        
        update_noti_field = models.NotificationSample.update_noti_sample(db, noti_id, update_noti_data.dict(exclude_unset=True, exclude_none=True))
        if not update_noti_field:
            return exceptions.bad_request_error("An error ocurred while updating Notification Sample, Please try again")
        # update the data.
        db.add(update_noti_field)
        db.commit()
        db.refresh(update_noti_field)
        
    except Exception as e:
        return exceptions.server_error(str(e))
    
    return success_response.success_message(update_noti_field, "Notification Sample record was successfully updated")

         
    

        

            
        
        
        
    


