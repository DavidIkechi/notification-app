from .conftest import get_session, client_instance
from .seeder import *
import sys
sys.path.append("..")
from db import models
import uuid
from fastapi import status
# from fastapi.testclient import TestClient
# from apis.client import client_router
# from main import notification_app
import logging

# Add this line to configure logging
logging.basicConfig(level=logging.DEBUG)

def test_transport_channel_seeder(get_session):
    # first check if the table is empty.
    channel_types = models.TransportChannel.retrieve_channels(get_session)
    assert len(channel_types) == 0
    # populate the table with the transport types
    seed_transport_channel(get_session)
    channel_types = models.TransportChannel.retrieve_channels(get_session)
    assert len(channel_types) == 2

# testing if the transport channel with id exists   
def test_channel_id_exists(get_session):
    # populate the table with the transport types
    seed_transport_channel(get_session)
    # For EMAILS
    get_channel = models.TransportChannel.get_channel_by_id(get_session, 1)
    assert get_channel is not None
    assert get_channel.id == 1
    assert get_channel.slug == "email"
    # FOR SMS
    get_channel = models.TransportChannel.get_channel_by_id(get_session, 2)
    assert get_channel is not None
    assert get_channel.id == 2
    assert get_channel.slug == "sms"

# testing if the transport channel with such id doesn't exist.    
def test_channel_id_not_exist(get_session):
    # populate the table with the transport types
    seed_transport_channel(get_session)
    # For EMAILS
    get_channel = models.TransportChannel.get_channel_by_id(get_session, 4)
    assert get_channel is None

# test if transport channel with slug name exists   
def test_channel_slug_exist(get_session):
    # populate the table with the transport types
    seed_transport_channel(get_session)
    # For EMAILS
    get_channel = models.TransportChannel.get_channel_by_slug(get_session, "email")
    assert get_channel is not None
    assert get_channel.id == 1
    # for SMS
    get_channel = models.TransportChannel.get_channel_by_slug(get_session, "sms")
    assert get_channel is not None
    assert get_channel.id == 2
    
def test_channel_slug_not_exists(get_session):
    seed_transport_channel(get_session)
    get_channel = models.TransportChannel.get_channel_by_slug(get_session, "phone")
    assert get_channel is None
    
    
    
    
    
