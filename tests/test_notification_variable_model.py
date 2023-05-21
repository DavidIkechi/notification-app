from .conftest import get_session
from .seeder import (
    seed_notification_type,
    seed_notification_variable
)
import sys
sys.path.append("..")
from utils import exclude_none_values
from db.models import NotificationVariables
from schema import *
import os
import uuid

def test_seed_notification_variable(get_session):
    # first populate the notificaton_type and notificatin variables
    seed_notification_type(get_session)
    seed_notification_variable(get_session)
    
    # check if it was added.
    noti_variables = NotificationVariables.retrieve_notification_variables(get_session)
    
    assert len(noti_variables) == 5
    
def test_get_single_variables(get_session):
    # first populate the notificaton_type and notificatin variables
    seed_notification_type(get_session)
    seed_notification_variable(get_session)
    
    # get the notification.
    get_variable = NotificationVariables.get_notification_variable_by_slug(get_session, 'login')
    assert get_variable is not None
    assert get_variable.noti_variable == [1, 2, 5, 6, 10, 8, 9, 7]
    