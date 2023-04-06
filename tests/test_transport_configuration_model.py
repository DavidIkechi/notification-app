from .conftest import get_session
from .seeder import *
import sys
sys.path.append("..")
from db import models
from schema import *
import uuid
from .test_notification_sample import get_notification_data, get_client_data 
import os

def trans_config_data():
    config_data = [
        {"client_id": 1, "trans_channel_id": 1, "trans_method": "smtp-email", "trans_config":
            {"mail_server": "smtp.google.com", "mail_username": "intuitive",
             "mail_password": "intuitive", "smtp_port": 567,
             "mail_tls": True, "mail_ssl": False}},
        {"client_id": 1, "trans_channel_id": 2, "trans_method": "twilio-sms", "trans_config":
            {"account_sid": "3ewfsrdsvehs", "auth_token": "er34ttedgu34ug",
             "sender_number": "8085463728"}}
        ]
    
    return config_data

def test_create_config(get_session):
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
    # get the data added.
    single_config = models.TransportConfiguration.get_transport_config_by_id(get_session, 1)
    assert single_config.client_id == 1
    assert single_config.trans_channel_id == 1
    # ensure that the keys are the same with the expected parameters entered    
    assert list(single_config.trans_config.keys()) == list(config_data['trans_config'].keys())
    # ensure that the configuration data for method and transport channel configuration are the same
    assert single_config.trans_method == config_data['trans_method']
    assert single_config.trans_config == config_data['trans_config']

def test_get_transport_config_by_channel_id(get_session):
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
    # add the sms_config_data for client
    config_data = trans_config_data()[1]
    config_data_schema = TransportConfigSchema(**config_data)
    # create the data.
    trans_config = models.TransportConfiguration.create_transport_config(
        get_session, config_data_schema.dict(exclude_unset=True, exclude_none=True))
    get_session.add(trans_config)
    get_session.commit()
    # check that it was added.
    retrieve_configs = models.TransportConfiguration.retrieve_transport_configs(get_session)
    assert len(retrieve_configs.all()) == 2
    # retrieve by channel_id.
    config = models.TransportConfiguration.get_transport_cconfig_by_channel_id(get_session, 1, 1)
    assert len(config.all()) == 1
    
def test_get_transport_config_by_trans_state(get_session):
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
    # add the sms_config_data for client
    config_data = trans_config_data()[1]
    config_data_schema = TransportConfigSchema(**config_data)
    # create the data.
    trans_config = models.TransportConfiguration.create_transport_config(
        get_session, config_data_schema.dict(exclude_unset=True, exclude_none=True))
    get_session.add(trans_config)
    get_session.commit()
    # check that it was added.
    retrieve_configs = models.TransportConfiguration.retrieve_transport_configs(get_session)
    assert len(retrieve_configs.all()) == 2
    # retrieve by Transport states.
    # Inactive 
    config = models.TransportConfiguration.get_transport_config_by_trans_state(get_session, 1, False)
    assert len(config.all()) == 0
    # active
    config = models.TransportConfiguration.get_transport_config_by_trans_state(get_session, 1, True)
    assert len(config.all()) == 2
    
def test_get_transport_config_by_trans_method(get_session):
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
    # get the transport config by method.
    config = models.TransportConfiguration.get_transport_config_by_method(get_session, 1, "smtp-email")
    assert config is not None
    
def test_get_transport_config_by_client_id(get_session):
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
    # get the transport config by method.
    config = models.TransportConfiguration.get_transport_configs_by_client_id(get_session, 1)
    assert len(config.all()) == 1
    
def test_update_transport_config_data(get_session):
    update_data ={
        "trans_config": {"mail_server": "blab", "mail_username": os.getenv('MAIL_USERNAME'), 
                         "mail_password": os.getenv('MAIL_PASSWORD'), "smtp_port": os.getenv('SMTP_PORT'), 
                         "mail_tls": os.getenv('MAIL_TLS'), "mail_ssl": os.getenv('MAIL_SSL')},
        "transport_state": False
    }
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
    
    # get the data added.
    single_config = models.TransportConfiguration.get_transport_config_by_id(get_session, 1)
    assert single_config.client_id == 1
    assert single_config.trans_channel_id == 1
    assert single_config.transport_state == True
    assert single_config.trans_config['mail_server'] == "smtp.google.com"
    # update the schema.
    update_config_schema = TransportConfigUpdateSchema(**update_data)
    updated_noti = models.TransportConfiguration.update_transport_config(get_session, 1, update_config_schema.dict(exclude_unset=True, exclude_none=True))
    get_session.commit()
    get_session.refresh(updated_noti)
    # check if the data was updated.
    single_config = models.TransportConfiguration.get_transport_config_by_id(get_session, 1)
    assert single_config.client_id == 1
    assert single_config.trans_channel_id == 1
    assert single_config.transport_state == False
    assert single_config.trans_config['mail_server'] == "blab"
    
def test_deactivate_transport_config_data(get_session):
    update_data ={
        "transport_state": False
    }
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
    
    # get the data added.
    single_config = models.TransportConfiguration.get_transport_config_by_id(get_session, 1)
    assert single_config.transport_state == True
    # update the schema.
    update_config_schema = TransportConfigUpdateSchema(**update_data)
    updated_noti = models.TransportConfiguration.update_transport_config(get_session, 1, update_config_schema.dict(exclude_unset=True, exclude_none=True))
    get_session.commit()
    get_session.refresh(updated_noti)
    # check if the data was updated.
    single_config = models.TransportConfiguration.get_transport_config_by_id(get_session, 1)
    assert single_config.transport_state == False
    