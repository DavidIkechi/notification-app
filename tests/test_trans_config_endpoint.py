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
    # see all necessary data
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
    
 
    