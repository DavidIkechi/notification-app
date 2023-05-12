from .conftest import get_session
from .seeder import (
    seed_transport_channel, seed_channel_transport,
    seed_notification_type, seed_client,
    seed_transport_configuration
)
import sys
sys.path.append("..")
from db.models import ActiveChannelClientConfig
from schema import *
import os

def test_create_active_channel(get_session):
    # first populate the transport channel and transport type tables
    seed_transport_channel(get_session)
    seed_notification_type(get_session)
    seed_channel_transport(get_session)
    seed_client(get_session)
    seed_transport_configuration(get_session)
    
    active_client_data = {
        "client_id": 1, "trans_channel_id": 1, "trans_config_id": 1
    }
    #check that it is empty.
    retrieve_active_client = ActiveChannelClientConfig.retrieve_active_channels(get_session)
    assert len(retrieve_active_client.all()) == 0
    # create the active client
    active_client = ActiveChannelClientConfig.create_active_channel(
        get_session, active_client_data)
    get_session.add(active_client)
    get_session.commit()
    # check that it was added.
    retrieve_active_client = ActiveChannelClientConfig.retrieve_active_channels(get_session)
    assert len(retrieve_active_client.all()) == 1
    # get the client by id
    get_active_client = ActiveChannelClientConfig.get_active_channel_by_id(get_session, 1)
    assert get_active_client.client_id == 1
    assert get_active_client.trans_channel_id == 1
    assert get_active_client.trans_config_id == 1
    
    
def test_get_active_client_by_client_trans_channel_id(get_session):
    # first populate the transport channel and transport type tables
    seed_transport_channel(get_session)
    seed_notification_type(get_session)
    seed_channel_transport(get_session)
    seed_client(get_session)
    seed_transport_configuration(get_session)
    
    active_client_data = {
        "client_id": 1, "trans_channel_id": 1, "trans_config_id": 1
    }
    # create the active client
    active_client = ActiveChannelClientConfig.create_active_channel(
        get_session, active_client_data)
    get_session.add(active_client)
    get_session.commit()
    # get the client by id
    get_client_config = ActiveChannelClientConfig.get_active_channel_by_client_tran_id(
        get_session, active_client_data['client_id'], active_client_data['trans_channel_id'])
    
    assert get_client_config is not None
    # check if it's only 1 record at first.
    assert len(get_client_config.all()) == 1
    get_client_config = get_client_config.first()
    
    assert get_client_config.trans_channel.slug == "email"
    # check if it's the actual method
    assert get_client_config.trans_config.trans_method == "smtp-email"
    assert get_client_config.trans_config.trans_config == {"mail_server": "smtp.gmail.com", "mail_username": "Intuitive", "mail_password": "heeiovmgrudlmtvi", "smtp_port": 567,
                                                           "mail_tls": True, "mail_ssl": False}