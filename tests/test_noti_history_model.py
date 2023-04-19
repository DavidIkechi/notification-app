from .conftest import get_session
from .seeder import (
    seed_transport_channel, seed_channel_transport,
    seed_notification_type, seed_client,
    seed_transport_configuration, seed_notification_sample,
    seed_active_channel_client_config
)
import sys
sys.path.append("..")
from utils import exclude_none_values, Status
from db.models import NotificationHistory, NotificationSample
from schema import *
import os
import uuid

def test_create_noti_history(get_session):
    # first populate the transport channel and transport type tables
    seed_transport_channel(get_session)
    seed_notification_type(get_session)
    seed_channel_transport(get_session)
    seed_client(get_session)
    seed_transport_configuration(get_session)
    seed_notification_sample(get_session)
    
    seed_active_channel_client_config(get_session)
    
    # add the email nootification for client in the notification history table.
    noti_sample = NotificationSample.get_noti_sample_by_id(get_session, 1)
    assert noti_sample is not None
    # get noti_data.
    # client_id, trans_channel_id, noti_type_id, sender_id, message_body
    noti_data ={
        'client_id': noti_sample.client_id,
        'trans_channel_id': noti_sample.trans_channel_id,
        'noti_type_id': noti_sample.noti_type_id,
        'message_body': noti_sample.message_body,
        'subject': noti_sample.subject,
        'sender_id': noti_sample.sender_id,
        'sender_email': noti_sample.sender_email,
        'carbon_copy': noti_sample.carbon_copy,
        'blind_copy': noti_sample.blind_copy
    }
    
    # exclude none values
    noti_sample_data = exclude_none_values(noti_data)
    # store it in the NotificationHistory Table
    # first check if the table is empty.
    noti_history = NotificationHistory.retrieve_noti_histories(get_session)
    assert len(noti_history.all()) == 0
    
    # insert now;
    new_noti_history = NotificationHistory.create_notification_history(get_session, noti_sample_data)
    get_session.add(new_noti_history)
    get_session.commit()
    
    noti_history = NotificationHistory.retrieve_noti_histories(get_session)
    assert len(noti_history.all()) == 1
    # check if it was added
    get_noti_history = NotificationHistory.get_noti_history_by_id(get_session, 1)
    assert get_noti_history is not None
    assert get_noti_history.status.value == "queue"
    assert get_noti_history.message_status is None 
    assert get_noti_history.rabbit_id is None
    

def test_update_noti_history(get_session):
    # first populate the transport channel and transport type tables
    seed_transport_channel(get_session)
    seed_notification_type(get_session)
    seed_channel_transport(get_session)
    seed_client(get_session)
    seed_transport_configuration(get_session)
    seed_notification_sample(get_session)
    
    seed_active_channel_client_config(get_session)
    # add the email nootification for client in the notification history table.
    noti_sample = NotificationSample.get_noti_sample_by_id(get_session, 1)
    assert noti_sample is not None
    # get the data: client_id, trans_channel_id, noti_type_id, sender_id, message_body
    noti_data ={
        'client_id': noti_sample.client_id,
        'trans_channel_id': noti_sample.trans_channel_id,
        'noti_type_id': noti_sample.noti_type_id,
        'message_body': noti_sample.message_body,
        'subject': noti_sample.subject,
        'sender_id': noti_sample.sender_id,
        'sender_email': noti_sample.sender_email,
        'carbon_copy': noti_sample.carbon_copy,
        'blind_copy': noti_sample.blind_copy
    }
    
    # exclude none values
    noti_sample_data = exclude_none_values(noti_data)
    # insert now;
    new_noti_history = NotificationHistory.create_notification_history(get_session, noti_sample_data)
    get_session.add(new_noti_history)
    get_session.commit()
    # check if it was added
    get_noti_history = NotificationHistory.get_noti_history_by_id(get_session, 1)
    assert get_noti_history is not None
    assert get_noti_history.status.value == "queue"
    assert get_noti_history.message_status is None 
    assert get_noti_history.rabbit_id is None
    
    # update data.
    update_noti_data = {
        "message_status": "Sent Successfully",
        "status": Status.SUCCESS,
        "rabbit_id": str(uuid.uuid4())
    }
    
    update_noti = NotificationHistory.update_notification_history(get_session, 1, update_noti_data)
    get_session.add(update_noti)
    get_session.commit()
    get_noti_history = NotificationHistory.get_noti_history_by_id(get_session, 1)
    assert get_noti_history is not None
    assert get_noti_history.status.value == "success"
    assert get_noti_history.message_status == "Sent Successfully" 
    assert get_noti_history.rabbit_id == update_noti_data['rabbit_id']
