from .conftest import get_session, client_instance
from .seeder import *
import sys
sys.path.append("..")
from db import models
import uuid
from fastapi import status


import logging

# Add this line to configure logging
logging.basicConfig(level=logging.DEBUG)

def test_notification_seeder(get_session):
    # first check if the table is empty.
    noti_types = models.NotificationType.retrieve_all_noti_type(get_session)
    assert len(noti_types) == 0
    # populate the table with the transport types
    seed_notification(get_session)
    noti_types = models.NotificationType.retrieve_all_noti_type(get_session)
    assert len(noti_types) == 4
    
def test_notification_type_id_exists(get_session):
    # populate the table with the notification types
    seed_notification(get_session)
    # check if id exists. for id = 1
    notification_type = models.NotificationType.get_noti_by_id(get_session, 1)
    assert notification_type is not None
    assert notification_type.noti_type == "Login"
    # for id = 2
    notification_type = models.NotificationType.get_noti_by_id(get_session, 2)
    assert notification_type is not None
    assert notification_type.noti_type == "Forgot Password"
    
    
def test_notification_type_id_not_exist(get_session):
    # populate the table with the notification types
    seed_notification(get_session)
    # check the ID.
    notification_type = models.NotificationType.get_noti_by_id(get_session, 6)
    assert notification_type is None
    
def test_notification_type_exist(get_session):
    # populate the table with the notification types
    seed_notification(get_session)
    notification_type = models.NotificationType.get_noti_by_type(get_session, "Login")
    assert notification_type is not None
    
    
def test_notification_type_not_exist(get_session):
    # populate the table with the notification types
    seed_notification(get_session)
    notification_type = models.NotificationType.get_noti_by_type(get_session, "Birthday Event")
    assert notification_type is None
   