from .conftest import get_session
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

def test_channel_transport_seeder(get_session):
    # first check if the table is empty.
    channel_transport = models.ChannelTransportType.retrieve_gateways(get_session)
    assert len(channel_transport) == 0
    # populate the table with the channel transport types
    seed_transport_channel(get_session)
    seed_channel_transport(get_session)
    channel_transport = models.ChannelTransportType.retrieve_gateways(get_session)
    assert len(channel_transport) == 4
    
def test_channel_transport_id_exist(get_session):
    # populate the table with the channel transport types
    seed_transport_channel(get_session)
    seed_channel_transport(get_session)
    # test id = 1
    channel_transport = models.ChannelTransportType.get_channel_trans_params_by_id(get_session, 1)
    assert channel_transport is not None
    assert channel_transport.slug == "smtp-email"
    # test id = 2
    channel_transport = models.ChannelTransportType.get_channel_trans_params_by_id(get_session, 2)
    assert channel_transport is not None
    assert channel_transport.slug == "twilio-sms" 
    
def test_channel_transport_id_not_exist(get_session):
    # populate the table with the channel transport types
    seed_transport_channel(get_session)
    seed_channel_transport(get_session)
    channel_transport = models.ChannelTransportType.get_channel_trans_params_by_id(get_session, 6)
    assert channel_transport is None
    
def test_channel_transport_slug_exist(get_session):
    # populate the table with the channel transport types
    seed_transport_channel(get_session)
    seed_channel_transport(get_session)
    # test id = 1
    channel_transport = models.ChannelTransportType.get_channel_trans_param_by_slug(get_session, "smtp-email")
    assert channel_transport is not None
    assert channel_transport.id == 1
    # test id = 2
    channel_transport = models.ChannelTransportType.get_channel_trans_param_by_slug(get_session, "twilio-sms")
    assert channel_transport is not None
    assert channel_transport.id == 2 
    
def test_channel_transport_slug_not_exist(get_session):
    # populate the table with the channel transport types
    seed_transport_channel(get_session)
    seed_channel_transport(get_session)
    channel_transport = models.ChannelTransportType.get_channel_trans_param_by_slug(get_session, "smtp-sms")
    assert channel_transport is None
    
def test_get_all_sms_channel_transports(get_session):
    # populate the table with the channel transport types
    seed_transport_channel(get_session)
    seed_channel_transport(get_session)
    
    get_channel = models.TransportChannel.get_channel_by_slug(get_session, "sms")
    assert get_channel is not None
    assert get_channel.id == 2
    assert len(get_channel.channel_trans) == 2
    
    assert get_channel.channel_trans[0].slug == "twilio-sms"
    assert get_channel.channel_trans[1].slug == "nexmo-sms"
    
def test_get_all_email_channel_transports(get_session):
    # populate the table with the channel transport types
    seed_transport_channel(get_session)
    seed_channel_transport(get_session)
    
    get_channel = models.TransportChannel.get_channel_by_slug(get_session, "email")
    assert get_channel is not None
    assert get_channel.id == 1
    assert len(get_channel.channel_trans) == 2
    
    assert get_channel.channel_trans[0].slug == "smtp-email"
    assert get_channel.channel_trans[1].slug == "mail-gun-email"
    
def test_check_email_gateway_transport_type(get_session):
    # populate the table with the channel transport types
    seed_transport_channel(get_session)
    seed_channel_transport(get_session)
    
    channel_transport = models.ChannelTransportType.get_channel_trans_param_by_slug(get_session, "smtp-email")
    assert channel_transport is not None
    assert channel_transport.id == 1
    assert channel_transport.trans_channel.slug == "email"
    
def test_check_sms_gateway_transport_type(get_session):
    # populate the table with the channel transport types
    seed_transport_channel(get_session)
    seed_channel_transport(get_session)
    
    channel_transport = models.ChannelTransportType.get_channel_trans_param_by_slug(get_session, "twilio-sms")
    assert channel_transport is not None
    assert channel_transport.id == 2
    assert channel_transport.trans_channel.slug == "sms"
    
    

    
    
    
    
    