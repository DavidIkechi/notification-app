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
from providers.sms.nexmo import NexmoGateway
from providers.sms.twilio import TwilioGateway
from providers.sms.main import SMSGate
from providers.email.smtp_mail import SMTPGateway



def look_up_history(db, hist_id):
    noti_data = NotificationHistory.get_noti_history_by_id(db, hist_id)
    config_data = ActiveChannelClientConfig.get_active_channel_by_client_tran_id(
        db, noti_data.client_id, noti_data.trans_channel_id).first()
    # get the trans_data.
    trans_data = config_data.trans_config.trans_config
    trans_data['sender_id'] = noti_data.sender_id
    trans_data['sender_email'] = noti_data.sender_email
    noti_dict = noti_data.__dict__
    noti_dict.pop("_sa_instance_state")  # remove non-serializable data
    noti_dict = exclude_none_values(noti_dict)

    # return both noti_data and trans_data.
    return noti_dict, trans_data
    


def test_send_noti_with_enabled_state(get_session, client_instance):
    # to enable notification state.
    updated_noti_data = {
        "notification_state": True
    }
    # seed the table with data.
    seed_client(get_session)
    seed_transport_channel(get_session)
    seed_notification_type(get_session)
    seed_notification_sample(get_session)
    seed_active_channel_client_config(get_session)
    
    # update to enabled!
    update_noti_schema = NotificationUpdateSchema(**updated_noti_data)
    updated_noti = NotificationSample.update_noti_sample(get_session, 1, update_noti_schema.dict(exclude_unset=True, exclude_none=True))
    get_session.commit()
    get_session.refresh(updated_noti)
    # header.
    headers = {
        "Client-Authorization": "new_key"
    }
    # notification data.
    update_data = {
        "noti_variables": {
            "firstname": "Mercy"
        },
        "recipients": [
            "davidakwuruu@gmail.com"
        ],
        "noti_type_slug": "welcome"
    }
    
    noti_response = client_instance.post("/notification/send/email", json=update_data, headers=headers)
    # assert noti_response.status_code == 200
    assert noti_response.json()['detail'] == "Notification has been triggered to be sent"

def test_send_noti_with_disabled_state(get_session, client_instance):
    # seed the table with data.
    seed_client(get_session)
    seed_transport_channel(get_session)
    seed_notification_type(get_session)
    seed_notification_sample(get_session)
    seed_active_channel_client_config(get_session)
    
    # header.
    headers = {
        "Client-Authorization": "new_key"
    }
    # notification data.
    update_data = {
        "noti_variables": {
            "firstname": "Mercy"
        },
        "recipients": [
            "davidakwuruu@gmail.com"
        ],
        "noti_type_slug": "welcome"
    }
    
    noti_response = client_instance.post("/notification/send/email", json=update_data, headers=headers)
    assert noti_response.status_code == 400
    assert noti_response.json()['detail'] == "Notification Sample is disabled!, Please enable to send" 
    
def test_send_noti_without_active_config(get_session, client_instance):
    # to enable notification state.
    updated_noti_data = {
        "notification_state": True
    }
    # seed the table with data.
    seed_client(get_session)
    seed_transport_channel(get_session)
    seed_notification_type(get_session)
    seed_notification_sample(get_session)
    # update to enabled!
    update_noti_schema = NotificationUpdateSchema(**updated_noti_data)
    updated_noti = NotificationSample.update_noti_sample(get_session, 1, update_noti_schema.dict(exclude_unset=True, exclude_none=True))
    get_session.commit()
    get_session.refresh(updated_noti)
    # header.
    headers = {
        "Client-Authorization": "new_key"
    }
    # notification data.
    update_data = {
        "noti_variables": {
            "firstname": "Mercy"
        },
        "recipients": [
            "davidakwuruu@gmail.com"
        ],
        "noti_type_slug": "welcome"
    }
    
    noti_response = client_instance.post("/notification/send/email", json=update_data, headers=headers)
    assert noti_response.status_code == 400
    assert noti_response.json()['detail'] == "No Active Transport Configuration has been set." 
        
def test_send_sms_success(get_session):
    # first seed the table. I want to use the email data.
    seed_client(get_session)
    seed_transport_channel(get_session)
    seed_notification_type(get_session)
    seed_notification_sample(get_session)
    seed_transport_configuration(get_session)
    seed_active_channel_client_config(get_session)
    seed_noti_history(get_session)

    # sms has been set to have an id of 2. in the seeder.
    noti_data, trans_data = look_up_history(get_session, hist_id=2)

    # Create a mock object for the Nexmo API client
    client_mock = MagicMock()
    send_message_mock = MagicMock(
        return_value={
            "messages": [
                {
                    "status": "0",
                    "message-id": "message-id-123",
                    "to": "recipient-number"
                }
            ]
        }
    )
    client_mock.sms.send_message = send_message_mock

    # Create an instance of NexmoGateway and replace the sms_config object with the mock
    nexmo_gateway = NexmoGateway(trans_data)
    nexmo_gateway.sms_config = client_mock

    # Call the send_sms method and check the response
    sms_result = asyncio.run(nexmo_gateway.send_sms(noti_data, trans_data))
    assert sms_result['status'] == 'success'
    assert sms_result['message_id'] == 'message-id-123'
    assert sms_result['recipient_number'] == 'recipient-number'
    

def test_send_email_success(get_session, mocker):
    # first seed the table. I want to use the email data.
    seed_client(get_session)
    seed_transport_channel(get_session)
    seed_notification_type(get_session)
    seed_notification_sample(get_session)
    seed_transport_configuration(get_session)
    seed_active_channel_client_config(get_session)
    seed_noti_history(get_session)
    
    # email has been set to have an id of 1. in the seeder.
    noti_data, trans_data = look_up_history(get_session, hist_id=1)
    
    # create the object.
    smtp_gateway = SMTPGateway(trans_data)
    
    # mock the FastMail instance and its send_message method
    mock_fastmail = mocker.patch.object(FastMail, "__init__")
    mock_fastmail.return_value = None
    mock_send_message = mocker.patch.object(FastMail, "send_message")
    mock_send_message.return_value = {"status": "success"}

    # Call the send_email method and check the response
    email_result = asyncio.run(smtp_gateway.send_email(noti_data, trans_data))
    assert email_result['status'] == 'success'
    assert email_result['message'] == "Email was sent successfully"
    assert email_result['recipient_number'] == noti_data['recipients']


    
    