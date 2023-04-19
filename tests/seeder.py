from sqlalchemy.orm import Session
import sys
sys.path.append("..")
import uuid

# functions to populate models
def seed_transport_channel(db: Session):
    # first check if the table is empty.
    from db.models import TransportChannel
    channel_type = [
        {"id":1, "channel_type": "email", "slug": "email"},
        {"id":2, "channel_type": "sms", "slug":"sms"}
    ]
    
    if TransportChannel.get_transport_channel_object(db).count() == 0:
        channel_instance = [TransportChannel(**channel) for channel in channel_type]
        db.add_all(channel_instance)
        db.commit()
        
def seed_notification_type(db: Session):
    from db.models import NotificationType
    notification_type = [
        {"id": 1, "noti_type": "Welcome", "slug": "welcome"},
        {"id": 2, "noti_type": "Login", "slug": "login"},
        {"id": 3, "noti_type": "Forgot Password", "slug": "forget-password"},
        {"id": 4, "noti_type": "Reset Password", "slug": "reset-password"},
        {"id": 5, "noti_type": "Registeration", "slug": "registeration"},
    ]
    
    if NotificationType.get_notification_object(db).count() == 0:
        notification_instance = [NotificationType(**notification) for notification in notification_type]
        db.add_all(notification_instance)
        db.commit()
      
def seed_channel_transport(db: Session):
    from db.models import ChannelTransportType
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
    
    if ChannelTransportType.get_channel_transport_object(db).count() == 0:
        gateway_instance = [ChannelTransportType(**channel) for channel in channel_gateway]
        db.add_all(gateway_instance)
        db.commit()
        
        
def seed_client(db: Session):
    from db.models import Client
    client_data = [
        {'slug': 'client-f','client_key': str(uuid.uuid4())}
    ]
    
    if Client.get_client_object(db).count() == 0:
        client_instance = [Client(**client) for client in client_data]
        db.add_all(client_instance)
        db.commit()
    

def seed_notification_sample(db: Session):
    from db.models import NotificationSample

    noti_data = [
        {'client_id': 1, 'trans_channel_id': 1, 'noti_type_id': 1, 'sender_id': 'Intutitve', 'message_body': "You are welcome"},
        {'client_id': 1, 'trans_channel_id': 2, 'noti_type_id': 2, 'sender_id': 'Intutitve', 'message_body': "An account just signed in"}
    ]
    if NotificationSample.noti_sample_object(db).count() == 0:
        noti_instance = [NotificationSample(**noti) for noti in noti_data]
        db.add_all(noti_instance)
        db.commit() 
        
def seed_transport_configuration(db: Session):
    from db.models import TransportConfiguration

    config_data = [
        {"client_id": 1, "trans_channel_id": 1, "trans_method": "smtp-email", "trans_config":
            {"mail_server": "smtp.google.com", "mail_username": "intuitive",
             "mail_password": "intuitive", "smtp_port": 567,
             "mail_tls": True, "mail_ssl": False}},
        {"client_id": 1, "trans_channel_id": 2, "trans_method": "twilio-sms", "trans_config":
            {"account_sid": "3ewfsrdsvehs", "auth_token": "er34ttedgu34ug",
             "sender_number": "8085463728"}}
    ]
    
    if TransportConfiguration.transport_config_object(db).count() == 0:
        trans_config_instance = [TransportConfiguration(**config) for config in config_data]
        db.add_all(trans_config_instance)
        db.commit()
    
def seed_active_channel_client_config(db: Session):
    from db.models import ActiveChannelClientConfig
    
    active_config = [
        {'client_id': 1, 'trans_channel_id': 1, 'trans_config_id': 1},
        {'client_id': 1, 'trans_channel_id': 2, 'trans_config_id': 2}
    ]
    
    if ActiveChannelClientConfig.active_channel_client_object(db).count() == 0:
        active_instance = [ActiveChannelClientConfig(**config) for  config in active_config]
        db.add_all(active_instance)
        db.commit()
        