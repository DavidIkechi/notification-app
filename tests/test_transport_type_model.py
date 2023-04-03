from .conftest import get_session
from .seeder import *
import sys
sys.path.append("..")
from db import models
import uuid
from fastapi import status


import logging

# Add this line to configure logging
logging.basicConfig(level=logging.DEBUG)

def test_transport_type_seeder(get_session):
    # first check if the table is empty.
    transport_types = models.TransportType.retrieve_transport_types(get_session)
    assert len(transport_types) == 0
    # populate the table with the transport types
    seed_transport_type(get_session)
    transport_types = models.TransportType.retrieve_transport_types(get_session)
    assert len(transport_types) == 5
    
def test_transport_type_id_exists(get_session):
    # populate the table with the notification types
    seed_transport_type(get_session)
    # check if id exists. for id = 1
    transport_type = models.TransportType.get_transport_by_id(get_session, 1)
    assert transport_type is not None
    assert transport_type.slug == "welcome"
    # for id = 2
    transport_type = models.TransportType.get_transport_by_id(get_session, 2)
    assert transport_type is not None
    assert transport_type.slug == "login"
    # for id = 3
    transport_type = models.TransportType.get_transport_by_id(get_session, 3)
    assert transport_type is not None
    assert transport_type.slug == "forget-password"
    # for id = 4
    transport_type = models.TransportType.get_transport_by_id(get_session, 4)
    assert transport_type is not None
    assert transport_type.slug == "reset-password"
    # for id = 5
    transport_type = models.TransportType.get_transport_by_id(get_session, 5)
    assert transport_type is not None
    assert transport_type.slug == "registeration"
    
    
def test_transport_type_id_not_exist(get_session):
    # populate the table with the notification types
    seed_transport_type(get_session)
    # check the ID.
    transport_type = models.TransportType.get_transport_by_id(get_session, 6)
    assert transport_type is None
    
def test_transport_slug_exist(get_session):
    # populate the table with the transport types
    seed_transport_type(get_session)
    # for welcome
    transport_type = models.TransportType.get_transport_by_slug(get_session, "welcome")
    assert transport_type is not None
    assert transport_type.id == 1
    # for login
    transport_type = models.TransportType.get_transport_by_slug(get_session, "login")
    assert transport_type is not None
    assert transport_type.id == 2
    # for forget password
    transport_type = models.TransportType.get_transport_by_slug(get_session, "forget-password")
    assert transport_type is not None
    assert transport_type.id == 3
    # for reset password
    transport_type = models.TransportType.get_transport_by_slug(get_session, "reset-password")
    assert transport_type is not None
    assert transport_type.id == 4
    # for registeration
    transport_type = models.TransportType.get_transport_by_slug(get_session, "registeration")
    assert transport_type is not None
    assert transport_type.id == 5
      
def test_transport_slug_not_exist(get_session):
    # populate the table with the transport types
    seed_transport_type(get_session)
    transport_type = models.TransportType.get_transport_by_slug(get_session, "register")
    assert transport_type is None   
    