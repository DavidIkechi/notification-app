from sqlalchemy.orm import Session
import sys
sys.path.append("..")
from db import models

# functions to populate models
def seed_transport_channel(db: Session):
    # first check if the table is empty.
    channel_type = [
        {"id":1, "channel_type": "email", "slug": "email"},
        {"id":2, "channel_type": "sms", "slug":"sms"}
    ]
    
    if models.TransportChannel.get_transport_channel_object(db).count() == 0:
        channel_instance = [models.TransportChannel(**channel) for channel in channel_type]
        db.add_all(channel_instance)
        db.commit()
        
def seed_transport_type(db: Session):
    transport_type = [
        {"id": 1, "trans_type": "Welcome", "slug": "welcome"},
        {"id": 2, "trans_type": "Login", "slug": "login"},
        {"id": 3, "trans_type": "Forgot Password", "slug": "forget-password"},
        {"id": 4, "trans_type": "Reset Password", "slug": "reset-password"},
        {"id": 5, "trans_type": "Registeration", "slug": "registeration"},
    ]
    
    if models.TransportType.get_transport_object(db).count() == 0:
        transport_instance = [models.TransportType(**transport) for transport in transport_type]
        db.add_all(transport_instance)
        db.commit()
        
def seed_channel_transport(db: Session):
    channel_gateway = [
        {"id": 1, "channel_id": 1, "gate_way": "SMTP EMAIL", "slug": "smtp-email",
         "parameters": ["mail_server", "mail_username", "mail_password", "smtp_port", "mail_tls", "mail_ssl"]},
        {"id": 2, "channel_id": 2, "gate_way": "TWILIO SMS", "slug": "twilio-sms",
         "parameters": ["account_sid", "auth_token", "sender_number"]},
        {"id": 3, "channel_id": 2, "gate_way": "NEXMO SMS", "slug": "nexmo-sms",
         "parameters": ["api_key", "secret_key", "sender_number"]},
        {"id": 4, "channel_id": 1, "gate_way": "MAIL GUN EMAIL", "slug": "mail-gun-email",
         "parameters":["mail_domain", "api_key"]}  
    ]
    
    if models.ChannelTransportType.get_channel_transport_object(db).count() == 0:
        gateway_instance = [models.ChannelTransportType(**channel) for channel in channel_gateway]
        db.add_all(gateway_instance)
        db.commit()
        
        
        