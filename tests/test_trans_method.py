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
    seed_noti_history
)

sys.path.append("..")
from db.models import (
    ActiveChannelClientConfig,
    TransportConfiguration
)
from schema import (
    NotificationDataSchema, 
    NotificationUpdateSchema,
    TransportConfigUpdateSchema
)

def test_get_methods(get_session, client_instance):
    # seed all necessary data.
    seed_client(get_session)
    seed_transport_channel(get_session)
    seed_notification_type(get_session)
    seed_notification_sample(get_session)
    seed_transport_configuration(get_session)  
    # add the header.
    headers = {
        "Client-Authorization": "new_key"
    }
    
    trans_response = client_instance.get("/transport_method/", headers=headers)    # assert len(noti_response.json()['data']['items'])== 2
    assert trans_response.status_code == 200
    assert len(trans_response.json()['data']['items'])== 4
    
def test_get_methods_per_channel(get_session, client_instance):
    # seed all necessary data.
    seed_client(get_session)
    seed_transport_channel(get_session)
    seed_notification_type(get_session)
    seed_notification_sample(get_session)
    seed_transport_configuration(get_session)  
    # add the header.
    headers = {
        "Client-Authorization": "new_key"
    }
    # add the queries parameters
    params = {
        "page": 1,
        "page_size": 10,
        "trans_type":"email"
    }
    trans_response = client_instance.get("/transport_method/", headers=headers, params=params)    # assert len(noti_response.json()['data']['items'])== 2
    assert trans_response.status_code == 200
    assert len(trans_response.json()['data']['items'])== 2
    
def test_get_transport_parameters(get_session, client_instance):
    # seed all necessary data.
    seed_client(get_session)
    seed_transport_channel(get_session)
    seed_notification_type(get_session)
    seed_notification_sample(get_session)
    seed_transport_configuration(get_session)
    
    # add the header.
    headers = {
        "Client-Authorization": "new_key"
    }
    # 
    trans_response = client_instance.get("/transport_method/parameters/smtp-email", headers=headers)
    assert trans_response.status_code == 200
    assert trans_response.json()['data'] == {'parameter':
        ["mail_server", "mail_username", "mail_password", "smtp_port", "mail_tls", "mail_ssl"]}
    
    