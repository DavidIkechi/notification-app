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

def test_create_transport_configuration(get_session, client_instance):
    # seed all necessary data.
    seed_client(get_session)
    seed_transport_channel(get_session)
    seed_notification_type(get_session)
    seed_notification_sample(get_session)    
    # add the header.
    headers = {
        "Client-Authorization": "new_key"
    }
    # delete all rows in the transport configuration table.
    get_session.query(TransportConfiguration).delete()
    get_session.commit()
    
    # check before putting new data. To ensure that it's actually empty.
    get_transport = TransportConfiguration.retrieve_transport_configs(get_session)
    assert len(get_transport.all()) == 0
    # configurationn data
    configuration_data = {
        "trans_channel": "email",
        "trans_type": "smtp-email",
        "trans_config": {
            "mail_ssl": True,
            "mail_tls": False,
            "smtp_port": 465,
            "mail_server": "#########",
            "mail_password": "##########",
            "mail_username": "#########"
        }
    }
    
    # create the transport confguration.
    trans_response = client_instance.post('/transport_configuration/create', 
                                           headers=headers, json=configuration_data)
    # force submit.
    get_session.commit()
    get_transport = TransportConfiguration.retrieve_transport_configs(get_session)
    assert len(get_transport.all()) == 1
    # check if the records were entered correctly.
    single_transport = TransportConfiguration.get_transport_config_by_id(
        get_session, 1)
    assert single_transport.trans_config == configuration_data['trans_config']
    assert single_transport.trans_method == configuration_data['trans_type']
    assert single_transport.trans_channel.slug == configuration_data['trans_channel']

def test_disable_transport_config(get_session, client_instance):
    # see all necessary data
    seed_client(get_session)
    seed_transport_channel(get_session)
    seed_notification_type(get_session)
    seed_notification_sample(get_session)
    seed_transport_configuration(get_session)
    
    # first check if was enabled initially.
    get_config = TransportConfiguration.get_transport_config_by_id(get_session, 1)
    assert get_config.transport_state == True
    assert get_config.trans_method == "smtp-email"
    # add the header.
    headers = {
        "Client-Authorization": "new_key"
    }
    # transport_method
    configuration_data = {
        "trans_type": "smtp-email"
    }
    # disable the transport confguration.
    trans_response = client_instance.patch('/transport_configuration/disable/email', 
                                           headers=headers, json=configuration_data)
    # force submit.
    get_session.commit()
    # first check if was disabled initially.
    get_config = TransportConfiguration.get_transport_config_by_id(get_session, 1)
    assert get_config.transport_state == False
    assert get_config.trans_method == "smtp-email"
    

def test_enable_transport_config(get_session, client_instance):
    update_data ={
        "transport_state": False
    }
    # see all necessary data
    seed_client(get_session)
    seed_transport_channel(get_session)
    seed_notification_type(get_session)
    seed_notification_sample(get_session)
    seed_transport_configuration(get_session)
    
        # update the schema.
    update_config_schema = TransportConfigUpdateSchema(**update_data)
    updated_noti = TransportConfiguration.update_transport_config(get_session, 1, update_config_schema.dict(exclude_unset=True, exclude_none=True))
    get_session.commit()
    get_session.refresh(updated_noti)  
    
    # first check if was enabled initially.
    get_config = TransportConfiguration.get_transport_config_by_id(get_session, 1)
    assert get_config.transport_state == False
    assert get_config.trans_method == "smtp-email"
    # add the header.
    headers = {
        "Client-Authorization": "new_key"
    }
    # transport_method
    configuration_data = {
        "trans_type": "smtp-email"
    }
    # disable the transport confguration.
    trans_response = client_instance.patch('/transport_configuration/enable/email', 
                                           headers=headers, json=configuration_data)
    # force submit.
    get_session.commit()
    # first check if was disabled initially.
    get_config = TransportConfiguration.get_transport_config_by_id(get_session, 1)
    assert get_config.transport_state == True
    assert get_config.trans_method == "smtp-email"
    
      
def test_active_transport_config(get_session, client_instance):
    # seed all necessary data
    seed_client(get_session)
    seed_transport_channel(get_session)
    seed_notification_type(get_session)
    seed_notification_sample(get_session)
    seed_transport_configuration(get_session) 

    # add the header.
    headers = {
        "Client-Authorization": "new_key"
    }
    # transport_method
    configuration_data = {
        "trans_type": "smtp-email"
    }
    # disable the transport confguration.
    trans_response = client_instance.put('/transport_configuration/activate/email', 
                                           headers=headers, json=configuration_data)
    # force submit.
    get_session.commit()
    # check if was added to the active client table.
    check_active = ActiveChannelClientConfig.get_active_channel_by_client_tran_id(
        get_session, 1, 1)
    
    assert len(check_active.all()) == 1
    # get the data
    check_active_data = check_active.first()
    assert check_active_data.client_id == 1
    assert check_active_data.trans_channel.slug == "email"
    

def test_update_transport_configuration(get_session, client_instance):
    # seed all necessary data
    seed_client(get_session)
    seed_transport_channel(get_session)
    seed_notification_type(get_session)
    seed_notification_sample(get_session)
    seed_transport_configuration(get_session) 

    # add the header.
    headers = {
        "Client-Authorization": "new_key"
    }
    # check the value before updating.
    single_transport = TransportConfiguration.get_transport_config_by_id(
        get_session, 1)
    # configurationn data
    assert single_transport.trans_config['smtp_port'] == 567
    assert single_transport.trans_config['mail_server'] == "smtp.gmail.com"
    
    configuration_data = {
        "trans_channel": "email",
        "trans_type": "smtp-email",
        "trans_config": {
            "mail_ssl": False,
            "mail_tls": True,
            "smtp_port": 587,
            "mail_server": "smtp.zoho.com",
            "mail_password": "#########",
            "mail_username": "#########"
        }
    }
    
    update_config =  client_instance.patch('/transport_configuration/update', 
                                           headers=headers, json=configuration_data)
    # force submit.
    get_session.commit()
    # check the value after updating.
    new_transport = TransportConfiguration.get_transport_config_by_id(
        get_session, 1)
    # configurationn data
    assert new_transport.trans_config['smtp_port'] == 587
    assert new_transport.trans_config['mail_server'] == "smtp.zoho.com"