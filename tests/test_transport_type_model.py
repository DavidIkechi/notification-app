from .conftest import get_session, client_instance
from .seeder import *
import sys
sys.path.append("..")
from db import models
from schema import ClientSchema, UpdateStatusSchema, UpdateClientKeySchema
import uuid
from fastapi import status
# from fastapi.testclient import TestClient
# from apis.client import client_router
# from main import notification_app
import logging

# Add this line to configure logging
logging.basicConfig(level=logging.DEBUG)

def test_transport_seeder(get_session):
    # first check if the table is empty.
    transport_types = models.TransportType.retrieve_all_transports(get_session)
    assert len(transport_types) == 0
    # populate the table with the transport types
    seed_transport(get_session)
    transport_types = models.TransportType.retrieve_all_transports(get_session)
    assert len(transport_types) == 2
    
def test_transport_id_exists(get_session):
    # populate the table with the transport types
    seed_transport(get_session)
    # For EMAILS
    get_transport = models.TransportType.get_transport_by_id(get_session, 1)
    assert get_transport is not None
    assert get_transport.id == 1
    assert get_transport.transport_type == "email"
    # FOR SMS
    get_transport = models.TransportType.get_transport_by_id(get_session, 2)
    assert get_transport is not None
    assert get_transport.id == 2
    assert get_transport.transport_type == "sms"
    
def test_transport_id_not_exist(get_session):
    # populate the table with the transport types
    seed_transport(get_session)
    # For EMAILS
    get_transport = models.TransportType.get_transport_by_id(get_session, 3)
    assert get_transport is None
    
def test_transport_name_exist(get_session):
    # populate the table with the transport types
    seed_transport(get_session)
    # For EMAILS
    get_transport = models.TransportType.get_transport_by_name(get_session, "email")
    assert get_transport is not None
    # for SMS
    get_transport = models.TransportType.get_transport_by_name(get_session, "sms")
    assert get_transport is not None
    
def test_transport_name_not_exists(get_session):
    seed_transport(get_session)
    # For EMAILS
    get_transport = models.TransportType.get_transport_by_name(get_session, "phone")
    assert get_transport is None
    
    
    
    
    
