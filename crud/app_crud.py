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
from schema import (
    NotificationDataSchema
)
from db.models import NotificationSample
from sqlalchemy.orm import load_only, joinedload, selectinload
from sqlalchemy import and_

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
        page_offset = Params(page=page, size=page_size)

        data_result = paginate(client_object, page_offset)
      
        return success_response.success_message(data_result)
        
    except Exception as e:
        return exceptions.server_error(str(e))
    
    
def create_noti_sample(db, client_id, noti_schema):
    try:
        # get the client_id, and noti_type_id and trans_channel_id
        client = models.Client.get_client_object(db).filter_by(slug=noti_schema.client_slug).first()
        noti_type = models.NotificationType.get_notification_by_slug(db, noti_schema.noti_type_slug)
        trans_type = models.TransportChannel.get_channel_by_slug(db, noti_schema.trans_channel_slug)
        
        if client is None:
            return exceptions.bad_request_error("Client with such slug doesn't Exist")
        
        if noti_type is None:
            return exceptions.bad_request_error("Notification Type with such slug doesn't Exist")
        
        if trans_type is None:
            return exceptions.bad_request_error("Transport Channel with such slug doesn't Exist")
        
        # get the ids
        trans_channel_id = trans_type.id
        noti_type_id = noti_type.id
        # Convert the instance to a dictionary
        data_dict = dict(noti_schema)

        # Update the dictionary keys to match NotificationDataSchema
        data_dict['client_id'] = client_id
        data_dict['trans_channel_id'] = trans_channel_id
        data_dict['noti_type_id'] = noti_type_id
        
        # check if it tallies with the new schema.
        noti_schema = NotificationDataSchema(**data_dict)

        # first check if the client_id matches with id passed.
        if client_id != client.id:
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

def send_notification(db, client_id: int, trans_channel_slug: str, sche_variables):
    try:
         # check if the noti matches the client.
        noti_type = models.NotificationType.get_notification_by_slug(db, sche_variables.noti_type_slug)
        trans_type = models.TransportChannel.get_channel_by_slug(db, trans_channel_slug)
        
        if noti_type is None:
            return exceptions.bad_request_error("Notification Type with such slug doesn't Exist")
        
        if trans_type is None:
            return exceptions.bad_request_error("Transport Channel with such slug doesn't Exist")
        
        # get the ids
        trans_channel_id = trans_type.id
        noti_type_id = noti_type.id
        
        check_noti = models.NotificationSample.check_noti_sample_by_noti_type_tran(
            db, client_id, noti_type_id, trans_channel_id)
                                                                                   
        if check_noti is None:
            return exceptions.bad_request_error("Notification with such ID doesn't exists")
        
        if check_noti.client_id != client_id:
            return exceptions.bad_request_error("Client ID is not associated with Notification Sample type")
        
        # check if the notification is disabled.
        if not check_noti.notification_state:
            return exceptions.bad_request_error("Notification Sample is disabled!, Please enable to send")
        # check if the configuration is active.
        check_config = models.ActiveChannelClientConfig.get_active_channel_by_client_tran_id(
            db, client_id, check_noti.trans_channel_id
        ).first()
        
        if check_config is None:
            return exceptions.bad_request_error("No Active Transport Configuration has been set.")
        # check if it is active or not as well
        if not check_config.trans_config.transport_state:
            return exceptions.bad_request_error("Transport Gateway is disabled!")
        # prepare the data;
        prepared_noti_data = get_noti_data(check_noti, sche_variables)
        # save the data.
        store_noti_data = models.NotificationHistory.create_notification_history(db, prepared_noti_data)
        db.add(store_noti_data)
        db.commit()
        db.refresh(store_noti_data)
        return success_response.success_message([], "Notification has been triggered to be sent")
            
    except Exception as e:
        return exceptions.server_error(str(e))
    
def update_noti_history(hist_id, update_data):
    try:
        # check if the data exists;
        check_noti_hist = models.NotificationHistory.get_noti_history_by_id(db, hist_id)
        if check_noti_hist is None:
            return exceptions.bad_request_error("Notification History with such ID doesn't exists")
        
        # proceed to update.
        update_noti_field = models.NotificationHistory.update_notification_history(db, hist_id, update_data)
        if not update_noti_field:
            return exceptions.bad_request_error("An error ocurred while updating Notification History, Please try again")
        # update the data.
        db.add(update_noti_field)
        db.commit()
        db.refresh(update_noti_field)
          
    except Exception as e:
        return exceptions.server_error(str(e))
    
    
def get_single_notification(db, client_id, noti_id):
    try:
        check_noti = models.NotificationSample.noti_sample_object(db).filter_by(
            id=noti_id, client_id=client_id).first()
        
        if check_noti is None:
            return exceptions.bad_request_error("Notification Sample Not found.")
    
    except Exception as e:
        return exceptions.server_error(str(e))
    
    return success_response.success_message(check_noti)


def get_all_notification(db, page: int, page_size: int, trans_type, client_id):
    try:
        # get the desired column.
        # get the notification object for the desired columns.
        noti_sample = models.NotificationSample.noti_sample_object(db).options(
            joinedload(models.NotificationSample.noti_type).load_only('slug').options(load_only('slug')),
            joinedload(models.NotificationSample.trans_channel).load_only('slug').options(load_only('slug')),
            load_only('id'),)
        
        if trans_type is None or trans_type.strip() == "":
            noti_result = noti_sample.filter_by(client_id=client_id)
        else:
            trans_channel = models.TransportChannel.get_channel_by_slug(db, trans_type.lower().strip())
            if trans_channel is None:
                return exceptions.bad_request_error("Transport Channel with such slug doesn't Exist")
     
            noti_result = noti_sample.filter_by(client_id=client_id, trans_channel_id=trans_channel.id)
            
        # calculate page offset.
        page_offset = Params(page=page, size=page_size)

        data_result = paginate(noti_result, page_offset)
        return success_response.success_message(data_result)
        
    except Exception as e:
        return exceptions.server_error(str(e))
    
def update_trans_config(db, client_id, trans_channel, trans_type, transport_state):
    try:
        # get the transport channel id.
        check_channel = models.TransportChannel.get_channel_by_slug(db, trans_channel.lower().strip())
        if check_channel is None:
            return exceptions.bad_request_error("Transport Channel with such slug doesn't Exist")
        
        trans_channel_id = check_channel.id
        # check if the transport method, client_id and trans_channel_id
        check_trans_config = models.TransportConfiguration.transport_config_object(
            db).filter_by(client_id=client_id, trans_channel_id=trans_channel_id, 
                          trans_method=trans_type.trans_type).first()
        
        if check_trans_config is None:
            return exceptions.bad_request_error("Transport Configuration type doesn't exist")
        # get the id
        trans_config_id = check_trans_config.id 
        # update the
        update_trans_config_field = models.TransportConfiguration.update_transport_config(db, trans_config_id, transport_state)
        if not update_trans_config_field:
            return exceptions.bad_request_error("An error ocurred while updating Transport Configuration, Please try again")
        # update the data.
        db.add(update_trans_config_field)
        db.commit()
        db.refresh(update_trans_config_field)
        
    except Exception as e:
        return exceptions.server_error(str(e))
    
    return success_response.success_message(update_trans_config_field, "Transport Configuration record was successfully updated")

def activate_trans_config(db, client_id, trans_channel, trans_type):
    try:
        # get the transport channel id.
        check_channel = models.TransportChannel.get_channel_by_slug(db, trans_channel.lower().strip())
        if check_channel is None:
            return exceptions.bad_request_error("Transport Channel with such slug doesn't Exist")
        
        trans_channel_id = check_channel.id
        # check if the transport method, client_id and trans_channel_id
        check_trans_config = models.TransportConfiguration.transport_config_object(
            db).filter_by(client_id=client_id, trans_channel_id=trans_channel_id, 
                          trans_method=trans_type.trans_type).first()
        
        if check_trans_config is None:
            return exceptions.bad_request_error("Transport Configuration type doesn't exist")
        # check if it's active.
        if not check_trans_config.transport_state:
            return exceptions.bad_request_error("Transport Configuration is not enabled or active")
            
        # get the id
        trans_config_id = check_trans_config.id
        
        # check if the user exist with same transport type.
        check_active_config = models.ActiveChannelClientConfig.get_active_channel_by_client_tran_id(
            db, client_id, trans_channel_id).first()
        
        active_data = {'client_id':client_id, 
                       'trans_channel_id':trans_channel_id, 
                       'trans_config_id': trans_config_id
                       } 
        
        if check_active_config is None:
            # create the transport.
            active_config = models.ActiveChannelClientConfig.create_active_channel(
                db, active_data)
        else:
            # update the transport.
            active_config = models.ActiveChannelClientConfig.update_active_channel(
                db, check_active_config.id, active_data)
            
        if not active_config:
            return exceptions.bad_request_error("An error ocurred while updating Transport Configuration, Please try again")
        # update the data.
        db.add(active_config)
        db.commit()
        db.refresh(active_config)
        
    except Exception as e:
        return exceptions.server_error(str(e))
    
    return success_response.success_message(active_config, "Transport Configuration was successfully activated!")