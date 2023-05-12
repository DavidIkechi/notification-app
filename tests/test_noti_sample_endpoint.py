from .conftest import get_session, client_instance
import sys
from .seeder import (
    seed_transport_channel,
    seed_notification_type,
    seed_client,
    seed_notification_sample
)

sys.path.append("..")
from db.models import NotificationSample
from schema import (
    NotificationDataSchema, 
    NotificationUpdateSchema
)
import uuid, json
from fastapi import status
# from fastapi.testclient import TestClient
# from apis.client import client_router
# from main import notification_app
import logging

def get_notification_data() -> list:
    noti_data = [
        {'client_slug': 'client-f', 'trans_channel_slug': 'email', 'noti_type_slug': 'welcome', 'sender_id': 'Intutitve', 'message_body': "Dear {{first_name}}, You are welcome"},
        {'client_slug': 'client-f', 'trans_channel_slug': 'sms', 'noti_type_slug': 'login', 'sender_id': 'Intutitve', 'message_body': "Dear {{first_name}}, An account just signed in"}
    ]
    
    return noti_data

def test_create_noti_sample_endpoint_with_middleware(get_session, client_instance):
    # seed the table with data.
    seed_client(get_session)
    seed_transport_channel(get_session)
    seed_notification_type(get_session)
    # header.
    headers = {
        "Client-Authorization": "new_key"
    }
    # get the data needed.
    email_noti_data = get_notification_data()[0]
    # get the notification router
    noti_response = client_instance.post("/notification/create", headers=headers, json=email_noti_data)
    assert noti_response.status_code == 201
    assert noti_response.json()['status'] == 1
    
def test_create_noti_sample_endpoint_without_middleware(get_session, client_instance):
    # seed the table with data.
    seed_client(get_session)
    seed_transport_channel(get_session)
    seed_notification_type(get_session)
    # get the data needed.
    email_noti_data = get_notification_data()[0]
    # get the notification router
    noti_response = client_instance.post("/notification/create", json=email_noti_data)
    assert noti_response.status_code == 401
    assert noti_response.json()['detail'] == "Client key is missing"

def test_enable_noti_sample_endpoint(get_session, client_instance):
    # seed the table with data.
    seed_client(get_session)
    seed_transport_channel(get_session)
    seed_notification_type(get_session)
    seed_notification_sample(get_session)
    # header.
    headers = {
        "Client-Authorization": "new_key"
    }
    # get the notification router
    noti_response = client_instance.patch(f"/notification/enable/1", headers=headers)
     # force commit after updating.
    get_session.commit()
    assert noti_response.status_code == 200
    
def test_disable_noti_sample_endpoint(get_session, client_instance):
    # seed the table with data.
    seed_client(get_session)
    seed_transport_channel(get_session)
    seed_notification_type(get_session)
    seed_notification_sample(get_session)
    # header.
    headers = {
        "Client-Authorization": "new_key"
    }
    # get the notification router
    noti_response = client_instance.patch(f'/notification/disable/1', headers=headers)
    # force commit after updating.
    get_session.commit()
    assert noti_response.status_code == 200
    
def test_update_noti_sample_endpoint(get_session, client_instance):
    # seed the table with data.
    seed_client(get_session)
    seed_transport_channel(get_session)
    seed_notification_type(get_session)
    seed_notification_sample(get_session)
    # header.
    headers = {
        "Client-Authorization": "new_key"
    }
    # first check the already saved data.
    get_sample = NotificationSample.get_noti_sample_by_id(get_session, 1)
    assert get_sample.sender_id == "Intuitive"
    assert get_sample.sender_email == None
    # prepare the data to be used for update.
    update_data = {
        "sender_email": "davidakwuruu@gmail.com",
        "sender_id": "Genesis Studio"
    }
    # update the notification sample with necessary information.
    noti_response = client_instance.patch(f'/notification/update/1', json=update_data, headers=headers)
    # force commit after updating.
    get_session.commit()  
    # check the updated data.
    get_sample = NotificationSample.get_noti_sample_by_id(get_session, 1)
    assert get_sample.sender_id == "Genesis Studio"
    assert get_sample.sender_email == "davidakwuruu@gmail.com"
    
def test_get_single_notification(get_session, client_instance):
    # seed the table with data.
    seed_client(get_session)
    seed_transport_channel(get_session)
    seed_notification_type(get_session)
    seed_notification_sample(get_session)
    # header.
    headers = {
        "Client-Authorization": "new_key"
    }
    # update the notification sample with necessary information.
    noti_response = client_instance.get(f'/notification/single/1', headers=headers)
    # force commit after updating.
    get_session.commit() 
    assert noti_response.status_code == 200
    
def test_get_all_client_notification(get_session, client_instance):
    # seed the table with data.
    seed_client(get_session)
    seed_transport_channel(get_session)
    seed_notification_type(get_session)
    seed_notification_sample(get_session)
    # header.
    headers = {
        "Client-Authorization": "new_key"
    }

    noti_response = client_instance.get("/notification/", headers=headers)    # assert len(noti_response.json()['data']['items'])== 2
    assert noti_response.status_code == 200
    assert len(noti_response.json()['data']['items'])== 2
    
def test_get_all_client_notification(get_session, client_instance):
    # seed the table with data.
    seed_client(get_session)
    seed_transport_channel(get_session)
    seed_notification_type(get_session)
    seed_notification_sample(get_session)
    # header.
    headers = {
        "Client-Authorization": "new_key"
    }
    params = {
        "page": 1,
        "page_size": 10,
        "trans_type":"email"
    }
    noti_response = client_instance.get("/notification/", headers=headers, params=params)    # assert len(noti_response.json()['data']['items'])== 2
    assert noti_response.status_code == 200
    assert len(noti_response.json()['data']['items'])== 1

    