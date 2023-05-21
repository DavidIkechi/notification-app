from .conftest import get_session, client_instance
from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
import sys
import asyncio
from .seeder import (
    seed_notification_type,
    seed_notification_variable,
    seed_client
)

sys.path.append("..")
from db.models import (
    NotificationSample,
    NotificationHistory,
    ActiveChannelClientConfig,
    NotificationVariables
)

def test_get_single_noti_variable(get_session, client_instance):
    # seed the database with the required data.
    seed_client(get_session)
    seed_notification_type(get_session)
    seed_notification_variable(get_session)
    
    # header.
    headers = {
        "Client-Authorization": "new_key"
    }
    # test the endpoint.
    noti_variable = client_instance.get('/variables/single/welcome', headers=headers)
    assert noti_variable.status_code == 200
    assert noti_variable.json()['detail'] == "Success"
    assert sorted(list(noti_variable.json()['data'].keys())) == sorted(['username', 'email_address', 'first_name', 'phone_number',
             'date', 'time', 'company_name'])