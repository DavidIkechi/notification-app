from .conftest import get_session, client_instance
from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
import sys
import asyncio
from .seeder import (
    seed_transport_channel,
    seed_notification_type,
    seed_client,
    seed_notification_sample,
    seed_transport_configuration,
    seed_active_channel_client_config,
    seed_noti_history,
    seed_notification_history
)

sys.path.append("..")
from db.models import (
    NotificationSample,
    NotificationHistory,
    ActiveChannelClientConfig
)
from schema import (
    NotificationDataSchema, 
    NotificationUpdateSchema
)
import uuid
from fastapi import status
from unittest.mock import MagicMock, patch, Mock
import logging
from utils import exclude_none_values

def test_get_single_client(get_session, client_instance):
    # first populate the transport channel and transport type tables
    seed_client(get_session)
    seed_transport_channel(get_session)
    seed_notification_type(get_session)
    seed_notification_sample(get_session)
    seed_transport_configuration(get_session)
    seed_active_channel_client_config(get_session)
    seed_notification_history(get_session)
    
    # get all the histories added.
    get_histories = NotificationHistory.retrieve_noti_histories(get_session)
    assert len(get_histories.all()) == 2
    
    # header.
    headers = {
        "Client-Authorization": "new_key"
    }
    
    noti_response = client_instance.get("/notification_history/single/1", headers=headers)
    assert noti_response.status_code == 200
    assert noti_response.json()['data']['sender_id'] == 'nnn'
    assert noti_response.json()['data']['trans_channel_id'] == 1
    assert noti_response.json()['data']['client_id'] == 1
    assert noti_response.json()['data']['resend'] == 0
    
def test_resend_noti_history(get_session, client_instance):
    # first populate the transport channel and transport type tables
    seed_client(get_session)
    seed_transport_channel(get_session)
    seed_notification_type(get_session)
    seed_notification_sample(get_session)
    seed_transport_configuration(get_session)
    seed_active_channel_client_config(get_session)
    seed_notification_history(get_session)
    
    # header.
    headers = {
        "Client-Authorization": "new_key"
    }
    # check if the resent is 0.
    get_noti = NotificationHistory.get_noti_history_by_id(get_session, 1)
    assert get_noti.resend == 0
    # hit the endpoint.
    noti_response = client_instance.patch('/notification_history/resend/1', headers=headers)
    # force commit
    get_session.commit()
    # check
    assert noti_response.status_code == 200
    # check if the resent is 1.
    get_noti = NotificationHistory.get_noti_history_by_id(get_session, 1)
    assert get_noti.resend == 1
    
def test_get_all_histories(get_session, client_instance):
    # first populate the transport channel and transport type tables
    seed_client(get_session)
    seed_transport_channel(get_session)
    seed_notification_type(get_session)
    seed_notification_sample(get_session)
    seed_transport_configuration(get_session)
    seed_active_channel_client_config(get_session)
    seed_notification_history(get_session)
    
    # header.
    headers = {
        "Client-Authorization": "new_key"
    }
    
    noti_response = client_instance.get('/notification_history/', headers=headers)
    assert noti_response.status_code == 200
    assert len(noti_response.json()['data']['items']) == 2
    
    
def test_get_all_histories_per_transport_type(get_session, client_instance):
    # first populate the transport channel and transport type tables
    seed_client(get_session)
    seed_transport_channel(get_session)
    seed_notification_type(get_session)
    seed_notification_sample(get_session)
    seed_transport_configuration(get_session)
    seed_active_channel_client_config(get_session)
    seed_notification_history(get_session)
    
    # header.
    headers = {
        "Client-Authorization": "new_key"
    }
    
    params = {
        "trans_type": "email"
    }
    
    noti_response = client_instance.get('/notification_history/', headers=headers, params=params)
    assert noti_response.status_code == 200
    assert len(noti_response.json()['data']['items']) == 1
    
    

