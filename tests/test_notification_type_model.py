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

def test_notification_type_seeder(get_session):
    # first check if the table is empty.
    notification_types = models.NotificationType.retrieve_notification_types(get_session)
    assert len(notification_types) == 0
    # populate the table with the notification types
    seed_notification_type(get_session)
    notification_types = models.NotificationType.retrieve_notification_types(get_session)
    assert len(notification_types) == 5
    
def test_notification_type_id_exists(get_session):
    # populate the table with the notification types
    seed_notification_type(get_session)
    # check if id exists. for id = 1
    notification_type = models.NotificationType.get_notification_by_id(get_session, 1)
    assert notification_type is not None
    assert notification_type.slug == "welcome"
    # for id = 2
    notification_type = models.NotificationType.get_notification_by_id(get_session, 2)
    assert notification_type is not None
    assert notification_type.slug == "login"
    # for id = 3
    notification_type = models.NotificationType.get_notification_by_id(get_session, 3)
    assert notification_type is not None
    assert notification_type.slug == "forget-password"
    # for id = 4
    notification_type = models.NotificationType.get_notification_by_id(get_session, 4)
    assert notification_type is not None
    assert notification_type.slug == "reset-password"
    # for id = 5
    notification_type = models.NotificationType.get_notification_by_id(get_session, 5)
    assert notification_type is not None
    assert notification_type.slug == "registeration"
    
    
def test_notification_type_id_not_exist(get_session):
    # populate the table with the notification types
    seed_notification_type(get_session)
    # check the ID.
    notification_type = models.NotificationType.get_notification_by_id(get_session, 6)
    assert notification_type is None
    
def test_notification_slug_exist(get_session):
    # populate the table with the notification types
    seed_notification_type(get_session)
    # for welcome
    notification_type = models.NotificationType.get_notification_by_slug(get_session, "welcome")
    assert notification_type is not None
    assert notification_type.id == 1
    # for login
    notification_type = models.NotificationType.get_notification_by_slug(get_session, "login")
    assert notification_type is not None
    assert notification_type.id == 2
    # for forget password
    notification_type = models.NotificationType.get_notification_by_slug(get_session, "forget-password")
    assert notification_type is not None
    assert notification_type.id == 3
    # for reset password
    notification_type = models.NotificationType.get_notification_by_slug(get_session, "reset-password")
    assert notification_type is not None
    assert notification_type.id == 4
    # for registeration
    notification_type = models.NotificationType.get_notification_by_slug(get_session, "registeration")
    assert notification_type is not None
    assert notification_type.id == 5
      
def test_notification_slug_not_exist(get_session):
    # populate the table with the notification types
    seed_notification_type(get_session)
    notification_type = models.NotificationType.get_notification_by_slug(get_session, "register")
    assert notification_type is None   
    