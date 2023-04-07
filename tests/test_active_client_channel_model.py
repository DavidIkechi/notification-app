from .conftest import get_session
from .seeder import *
import sys
sys.path.append("..")
from db import models
from schema import *
import uuid
from .test_notification_sample import get_notification_data, get_client_data 
from .test_transport_configuration_model import trans_config_data
import os

def test_create_active_channel(get_session):
    # first populate the transport channel and transport type tables
    seed_transport_channel(get_session)
    seed_notification_type(get_session)
    seed_channel_transport(get_session)
    # add the client
    client_1 = ClientSchema(**get_client_data())
    created_client_1 = models.Client.create_single_client(get_session, client_1.slug, client_1.client_key)
    get_session.add(created_client_1)
    get_session.commit()
    # add the email_config_data for client
    config_data = trans_config_data()[0]
    config_data_schema = TransportConfigSchema(**config_data)
    # create the data.
    trans_config = models.TransportConfiguration.create_transport_config(
        get_session, config_data_schema.dict(exclude_unset=True, exclude_none=True))
    get_session.add(trans_config)
    get_session.commit()
     # check that it was added.
    retrieve_configs = models.TransportConfiguration.retrieve_transport_configs(get_session)
    assert len(retrieve_configs.all()) == 1
    
    active_client_data = {
        "client_id": 1, "trans_channel_id": 1, "trans_config_id": 1
    }
    # create the active client
    active_client = models.ActiveChannelClientConfig.create_active_channel(
        get_session, active_client_data)
    get_session.add(active_client)
    get_session.commit()
    
    # check that it was added.
    retrieve_active_client = models.ActiveChannelClientConfig.retrieve_active_channels(get_session)
    assert len(retrieve_active_client.all()) == 1
    
def test_get_active_client_by_id(get_session):
    # first populate the transport channel and transport type tables
    seed_transport_channel(get_session)
    seed_notification_type(get_session)
    seed_channel_transport(get_session)
    # add the client
    client_1 = ClientSchema(**get_client_data())
    created_client_1 = models.Client.create_single_client(get_session, client_1.slug, client_1.client_key)
    get_session.add(created_client_1)
    get_session.commit()
    # add the email_config_data for client
    config_data = trans_config_data()[0]
    config_data_schema = TransportConfigSchema(**config_data)
    # create the data.
    trans_config = models.TransportConfiguration.create_transport_config(
        get_session, config_data_schema.dict(exclude_unset=True, exclude_none=True))
    get_session.add(trans_config)
    get_session.commit()
     # check that it was added.
    retrieve_configs = models.TransportConfiguration.retrieve_transport_configs(get_session)
    assert len(retrieve_configs.all()) == 1
    
    active_client_data = {
        "client_id": 1, "trans_channel_id": 1, "trans_config_id": 1
    }
    # create the active client
    active_client = models.ActiveChannelClientConfig.create_active_channel(
        get_session, active_client_data)
    get_session.add(active_client)
    get_session.commit()
    # get the client by id
    get_active_client = models.ActiveChannelClientConfig.get_active_channel_by_id(get_session, 1)
    assert get_active_client.client_id == 1
    assert get_active_client.trans_channel_id == 1
    
def test_get_active_client_by_client_id(get_session):
    # first populate the transport channel and transport type tables
    seed_transport_channel(get_session)
    seed_notification_type(get_session)
    seed_channel_transport(get_session)
    # add the client
    client_1 = ClientSchema(**get_client_data())
    created_client_1 = models.Client.create_single_client(get_session, client_1.slug, client_1.client_key)
    get_session.add(created_client_1)
    get_session.commit()
    # add the email_config_data for client
    config_data = trans_config_data()[0]
    config_data_schema = TransportConfigSchema(**config_data)
    # create the data.
    trans_config = models.TransportConfiguration.create_transport_config(
        get_session, config_data_schema.dict(exclude_unset=True, exclude_none=True))
    get_session.add(trans_config)
    get_session.commit()
     # check that it was added.
    retrieve_configs = models.TransportConfiguration.retrieve_transport_configs(get_session)
    assert len(retrieve_configs.all()) == 1
    
    active_client_data = {
        "client_id": 1, "trans_channel_id": 1, "trans_config_id": 1
    }
    # create the active client
    active_client = models.ActiveChannelClientConfig.create_active_channel(
        get_session, active_client_data)
    get_session.add(active_client)
    get_session.commit()
    # get the client by id
    get_active_client = models.ActiveChannelClientConfig.get_active_channel_by_client_id(get_session, active_client_data['client_id'])
    assert get_active_client is not None
    assert len(get_active_client) == 1
    
def test_get_active_client_config_by_trans_channel_id(get_session):
    # first populate the transport channel and transport type tables
    seed_transport_channel(get_session)
    seed_notification_type(get_session)
    seed_channel_transport(get_session)
    # add the client
    client_1 = ClientSchema(**get_client_data())
    created_client_1 = models.Client.create_single_client(get_session, client_1.slug, client_1.client_key)
    get_session.add(created_client_1)
    get_session.commit()
    # add the email_config_data for client
    config_data = trans_config_data()[0]
    config_data_schema = TransportConfigSchema(**config_data)
    # create the data.
    trans_config = models.TransportConfiguration.create_transport_config(
        get_session, config_data_schema.dict(exclude_unset=True, exclude_none=True))
    get_session.add(trans_config)
    get_session.commit()
     # check that it was added.
    retrieve_configs = models.TransportConfiguration.retrieve_transport_configs(get_session)
    assert len(retrieve_configs.all()) == 1
    
    active_client_data = {
        "client_id": 1, "trans_channel_id": 1, "trans_config_id": 1
    }
    # create the active client
    active_client = models.ActiveChannelClientConfig.create_active_channel(
        get_session, active_client_data)
    get_session.add(active_client)
    get_session.commit()
    # get the client by id
    get_client_config = models.ActiveChannelClientConfig.get_active_channel_by_client_tran_id(
        get_session, active_client_data['client_id'], active_client_data['trans_channel_id'])
    
    assert get_client_config is not None
    assert get_client_config.trans_channel.slug == "email"

def test_get_active_channels_by_transport(get_session):
    # first populate the transport channel and transport type tables
    seed_transport_channel(get_session)
    seed_notification_type(get_session)
    seed_channel_transport(get_session)
    # add the client
    client_1 = ClientSchema(**get_client_data())
    created_client_1 = models.Client.create_single_client(get_session, client_1.slug, client_1.client_key)
    get_session.add(created_client_1)
    get_session.commit()
    # add the email_config_data for client
    config_data = trans_config_data()[0]
    config_data_schema = TransportConfigSchema(**config_data)
    # create the data.
    trans_config = models.TransportConfiguration.create_transport_config(
        get_session, config_data_schema.dict(exclude_unset=True, exclude_none=True))
    get_session.add(trans_config)
    get_session.commit()
     # check that it was added.
    retrieve_configs = models.TransportConfiguration.retrieve_transport_configs(get_session)
    assert len(retrieve_configs.all()) == 1
    
    active_client_data = {
        "client_id": 1, "trans_channel_id": 1, "trans_config_id": 1
    }
    # create the active client
    active_client = models.ActiveChannelClientConfig.create_active_channel(
        get_session, active_client_data)
    get_session.add(active_client)
    get_session.commit()
    # get the client by id
    get_client_config = models.ActiveChannelClientConfig.retrieve_active_channels_by_trans_channel(
        get_session, active_client_data['trans_channel_id'])
    
    assert len(get_client_config.all()) == 1
    
def test_get_active_client_by_trans_config_id(get_session):
    # first populate the transport channel and transport type tables
    seed_transport_channel(get_session)
    seed_notification_type(get_session)
    seed_channel_transport(get_session)
    # add the client
    client_1 = ClientSchema(**get_client_data())
    created_client_1 = models.Client.create_single_client(get_session, client_1.slug, client_1.client_key)
    get_session.add(created_client_1)
    get_session.commit()
    # add the email_config_data for client
    config_data = trans_config_data()[0]
    config_data_schema = TransportConfigSchema(**config_data)
    # create the data.
    trans_config = models.TransportConfiguration.create_transport_config(
        get_session, config_data_schema.dict(exclude_unset=True, exclude_none=True))
    get_session.add(trans_config)
    get_session.commit()
     # check that it was added.
    retrieve_configs = models.TransportConfiguration.retrieve_transport_configs(get_session)
    assert len(retrieve_configs.all()) == 1
    
    active_client_data = {
        "client_id": 1, "trans_channel_id": 1, "trans_config_id": 1
    }
    # create the active client
    active_client = models.ActiveChannelClientConfig.create_active_channel(
        get_session, active_client_data)
    get_session.add(active_client)
    get_session.commit()
    # get the client by id
    get_active_client = models.ActiveChannelClientConfig.get_active_channel_by_trans_config_id(
        get_session, active_client_data['trans_config_id'])
    assert get_active_client.client_id == 1
    assert get_active_client.trans_channel_id == 1
    
    
    