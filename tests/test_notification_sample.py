from .conftest import get_session
from .seeder import *
import sys
sys.path.append("..")
from db import models
from schema import *
import uuid

def get_client_data() -> dict:
    client_data = {
        'slug': 'client-f',
        'client_key': str(uuid.uuid4())
    }
    
    return client_data
    

def get_notification_data() -> list:
    noti_data = [
        {'client_id': 1, 'trans_channel_id': 1, 'trans_type_id': 1, 'sender_id': 'Intutitve', 'message_body': "You are welcome"},
        {'client_id': 1, 'trans_channel_id': 2, 'trans_type_id': 2, 'sender_id': 'Intutitve', 'message_body': "An account just signed in"}
    ]
    
    return noti_data


def test_seeder_channel_transport_channel(get_session):
    # first populate the transport channel and transport type tables
    seed_transport_channel(get_session)
    seed_transport_type(get_session)
    
    channels = models.TransportChannel.retrieve_channels(get_session)
    transport_types = models.TransportType.retrieve_transport_types(get_session)
    
    assert len(channels) == 2
    assert len(transport_types) == 5
    
    
def test_create_email_noti_sample(get_session):
    # first populate the transport channel and transport type tables
    seed_transport_channel(get_session)
    seed_transport_type(get_session)
    # add the client
    client_1 = ClientSchema(**get_client_data())
    created_client_1 = models.Client.create_single_client(get_session, client_1.slug, client_1.client_key)
    get_session.add(created_client_1)
    get_session.commit()
    # get the notification data from the notification data function.
    email_noti_data = get_notification_data()[0]
    email_noti_schema = NotificationDataSchema(**email_noti_data)
    # create the data
    email_noti_sample = models.NotificationSample.create_noti_sample(get_session, email_noti_schema.dict(exclude_unset=True, exclude_none=True))
    get_session.add(email_noti_sample)
    get_session.commit()
    # check that it was added.
    retrieve_noti = models.NotificationSample.retrieve_noti_samples(get_session)
    assert len(retrieve_noti) == 1   
    #retrieve the email sample for the client.
    get_noti =models.NotificationSample.get_noti_sample_by_id(get_session, 1)
    assert get_noti is not None
    assert get_noti.client.client_key == client_1.client_key
    assert get_noti.trans_channel.slug == "email"
    

def test_create_sms_noti_sample(get_session):
    # first populate the transport channel and transport type tables
    seed_transport_channel(get_session)
    seed_transport_type(get_session)
    # add the client
    client_1 = ClientSchema(**get_client_data())
    created_client_1 = models.Client.create_single_client(get_session, client_1.slug, client_1.client_key)
    get_session.add(created_client_1)
    get_session.commit()
    # get the notification data from the notification data function.
    sms_noti_data = get_notification_data()[1]
    sms_noti_schema = NotificationDataSchema(**sms_noti_data)
    # create the data.
    sms_noti_sample = models.NotificationSample.create_noti_sample(get_session, sms_noti_schema.dict(exclude_unset=True, exclude_none=True))
    get_session.add(sms_noti_sample)
    get_session.commit()
    # check that it was added.
    retrieve_noti = models.NotificationSample.retrieve_noti_samples(get_session)
    assert len(retrieve_noti) == 1   
    #retrieve the email sample for the client.
    get_noti =models.NotificationSample.get_noti_sample_by_id(get_session, 1)
    assert get_noti is not None
    assert get_noti.client.client_key == client_1.client_key
    assert get_noti.trans_channel.slug == "sms"

def test_retrieve_noti_sample_by_status(get_session):
    # first populate the transport channel and transport type tables
    seed_transport_channel(get_session)
    seed_transport_type(get_session)
    # add the client
    client_1 = ClientSchema(**get_client_data())
    created_client_1 = models.Client.create_single_client(get_session, client_1.slug, client_1.client_key)
    get_session.add(created_client_1)
    get_session.commit()
     # add email-noti data
    email_noti_data = get_notification_data()[0]
    email_noti_schema = NotificationDataSchema(**email_noti_data)
    email_noti_sample = models.NotificationSample.create_noti_sample(get_session, email_noti_schema.dict(exclude_unset=True, exclude_none=True))
    get_session.add(email_noti_sample)
    get_session.commit()
    # add sms noti-data
    sms_noti_data = get_notification_data()[1]
    sms_noti_schema = NotificationDataSchema(**sms_noti_data)
    sms_noti_sample = models.NotificationSample.create_noti_sample(get_session, sms_noti_schema.dict(exclude_unset=True, exclude_none=True))
    get_session.add(sms_noti_sample)
    get_session.commit()
    # check that it was added.
    retrieve_noti = models.NotificationSample.retrieve_noti_samples(get_session)
    assert len(retrieve_noti) == 2
    # retrieve all notifications by their status for a client. i.e active(True) or inactive(False)
    active_notifications = models.NotificationSample.retrieve_noti_samples_by_status(get_session, 1, True)
    assert len(active_notifications.all()) == 2
    # inactive
    inactive_notifications = models.NotificationSample.retrieve_noti_samples_by_status(get_session, 1, False)
    assert len(inactive_notifications.all()) == 0
    

def test_retrieve_noti_samples_by_transport_channel(get_session):
     # first populate the transport channel and transport type tables
    seed_transport_channel(get_session)
    seed_transport_type(get_session)
    # add the client
    client_1 = ClientSchema(**get_client_data())
    created_client_1 = models.Client.create_single_client(get_session, client_1.slug, client_1.client_key)
    get_session.add(created_client_1)
    get_session.commit()
     # add email-noti data
    email_noti_data = get_notification_data()[0]
    email_noti_schema = NotificationDataSchema(**email_noti_data)
    email_noti_sample = models.NotificationSample.create_noti_sample(get_session, email_noti_schema.dict(exclude_unset=True, exclude_none=True))
    get_session.add(email_noti_sample)
    get_session.commit()
    # add sms noti-data
    sms_noti_data = get_notification_data()[1]
    sms_noti_schema = NotificationDataSchema(**sms_noti_data)
    sms_noti_sample = models.NotificationSample.create_noti_sample(get_session, sms_noti_schema.dict(exclude_unset=True, exclude_none=True))
    get_session.add(sms_noti_sample)
    get_session.commit()
    
    # transport channel indicates both sms and email.(sms has and id of 1, and email has an id of 1)
    sms_notifications = models.NotificationSample.retrieve_noti_samples_by_trans_channel(get_session, 1, 2)
    assert len(sms_notifications.all()) == 1
    # inactive
    email_notifications = models.NotificationSample.retrieve_noti_samples_by_trans_channel(get_session, 1, 1)
    assert len(email_notifications.all()) == 1
     
def test_retrieve_noti_samples_per_client(get_session):
     # first populate the transport channel and transport type tables
    seed_transport_channel(get_session)
    seed_transport_type(get_session)
    # add the client
    client_1 = ClientSchema(**get_client_data())
    created_client_1 = models.Client.create_single_client(get_session, client_1.slug, client_1.client_key)
    get_session.add(created_client_1)
    get_session.commit()
     # add email-noti data
    email_noti_data = get_notification_data()[0]
    email_noti_schema = NotificationDataSchema(**email_noti_data)
    email_noti_sample = models.NotificationSample.create_noti_sample(get_session, email_noti_schema.dict(exclude_unset=True, exclude_none=True))
    get_session.add(email_noti_sample)
    get_session.commit()
    
    client_noti_samples = models.NotificationSample.retrieve_all_noti_samples_by_client_id(get_session, 1)
    assert len(client_noti_samples.all()) == 1
    
def test_get_noti_sample_by_id_exists(get_session):
     # first populate the transport channel and transport type tables
    seed_transport_channel(get_session)
    seed_transport_type(get_session)
    # add the client
    client_1 = ClientSchema(**get_client_data())
    created_client_1 = models.Client.create_single_client(get_session, client_1.slug, client_1.client_key)
    get_session.add(created_client_1)
    get_session.commit()
     # add email-noti data
    email_noti_data = get_notification_data()[0]
    email_noti_schema = NotificationDataSchema(**email_noti_data)
    email_noti_sample = models.NotificationSample.create_noti_sample(get_session, email_noti_schema.dict(exclude_unset=True, exclude_none=True))
    get_session.add(email_noti_sample)
    get_session.commit()
    
    noti_sample = models.NotificationSample.get_noti_sample_by_id(get_session, 1)
    assert noti_sample.message_body == "You are welcome"
    assert noti_sample.created_at is not None
    assert noti_sample.updated_at is not None

def test_get_noti_sample_by_id_not_exists(get_session):
     # first populate the transport channel and transport type tables
    seed_transport_channel(get_session)
    seed_transport_type(get_session)
    # add the client
    client_1 = ClientSchema(**get_client_data())
    created_client_1 = models.Client.create_single_client(get_session, client_1.slug, client_1.client_key)
    get_session.add(created_client_1)
    get_session.commit()
     # add email-noti data
    email_noti_data = get_notification_data()[0]
    email_noti_schema = NotificationDataSchema(**email_noti_data)
    email_noti_sample = models.NotificationSample.create_noti_sample(get_session, email_noti_schema.dict(exclude_unset=True, exclude_none=True))
    get_session.add(email_noti_sample)
    get_session.commit()
    
    noti_sample = models.NotificationSample.get_noti_sample_by_id(get_session, 3)
    assert noti_sample is None

def test_update_noti_sample(get_session):
    updated_noti_data = {
        "carbon_copy": ["davidakwuruu@gmail.com"],
        "blind_copy": ["intuitive@gmail.com"],
        "notification_state": False
    }
    # first populate the transport channel and transport type tables
    seed_transport_channel(get_session)
    seed_transport_type(get_session)
    # add the client
    client_1 = ClientSchema(**get_client_data())
    created_client_1 = models.Client.create_single_client(get_session, client_1.slug, client_1.client_key)
    get_session.add(created_client_1)
    get_session.commit()
     # add email-noti data
    email_noti_data = get_notification_data()[0]
    email_noti_schema = NotificationDataSchema(**email_noti_data)
    email_noti_sample = models.NotificationSample.create_noti_sample(get_session, email_noti_schema.dict(exclude_unset=True, exclude_none=True))
    get_session.add(email_noti_sample)
    get_session.commit()
    # add sms noti-data
    sms_noti_data = get_notification_data()[1]
    sms_noti_schema = NotificationDataSchema(**sms_noti_data)
    sms_noti_sample = models.NotificationSample.create_noti_sample(get_session, sms_noti_schema.dict(exclude_unset=True, exclude_none=True))
    get_session.add(sms_noti_sample)
    get_session.commit()
    
    # first check the state.
    noti_sample = models.NotificationSample.get_noti_sample_by_id(get_session, 1)
    assert noti_sample.message_body == "You are welcome"
    assert noti_sample.carbon_copy == []
    assert noti_sample.blind_copy == []
    assert noti_sample.notification_state is True
    # update the sample
    update_noti_schema = NotificationUpdateSchema(**updated_noti_data)
    updated_noti = models.NotificationSample.update_noti_sample(get_session, 1, update_noti_schema.dict(exclude_unset=True, exclude_none=True))
    get_session.commit()
    get_session.refresh(updated_noti)
    # check the updated state.
    noti_sample = models.NotificationSample.get_noti_sample_by_id(get_session, 1)
    assert noti_sample.message_body == "You are welcome"
    assert noti_sample.carbon_copy == updated_noti_data['carbon_copy']
    assert noti_sample.blind_copy == updated_noti_data['blind_copy']
    assert noti_sample.notification_state is False
    
def test_disable_noti_sample(get_session):
    updated_noti_data = {
        "notification_state": False
    }
    # first populate the transport channel and transport type tables
    seed_transport_channel(get_session)
    seed_transport_type(get_session)
    # add the client
    client_1 = ClientSchema(**get_client_data())
    created_client_1 = models.Client.create_single_client(get_session, client_1.slug, client_1.client_key)
    get_session.add(created_client_1)
    get_session.commit()
     # add email-noti data
    email_noti_data = get_notification_data()[0]
    email_noti_schema = NotificationDataSchema(**email_noti_data)
    email_noti_sample = models.NotificationSample.create_noti_sample(get_session, email_noti_schema.dict(exclude_unset=True, exclude_none=True))
    get_session.add(email_noti_sample)
    get_session.commit()
    # first check the state.
    noti_sample = models.NotificationSample.get_noti_sample_by_id(get_session, 1)
    assert noti_sample.notification_state is True
    # update the sample
    update_noti_schema = NotificationUpdateSchema(**updated_noti_data)
    updated_noti = models.NotificationSample.update_noti_sample(get_session, 1, update_noti_schema.dict(exclude_unset=True, exclude_none=True))
    get_session.commit()
    get_session.refresh(updated_noti)
    # check the updated state.
    noti_sample = models.NotificationSample.get_noti_sample_by_id(get_session, 1)
    assert noti_sample.notification_state is False
    
    
    
    
   