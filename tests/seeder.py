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
         "parameters":["mail_domain", "mail_api_key"]}  
    ]
    
    if ChannelTransportType.get_channel_transport_object(db).count() == 0:
        gateway_instance = [ChannelTransportType(**channel) for channel in channel_gateway]
        db.add_all(gateway_instance)
        db.commit()
        
        
def seed_client(db: Session):
    from db.models import Client
    client_data = [
        {'slug': 'client-f','client_key': "new_key"}
    ]
    
    if Client.get_client_object(db).count() == 0:
        client_instance = [Client(**client) for client in client_data]
        db.add_all(client_instance)
        db.commit()
    

def seed_notification_sample(db: Session):
    from db.models import NotificationSample

    noti_data = [
        {'id':1, 'client_id': 1, 'trans_channel_id': 1, 'noti_type_id': 1, 'sender_id': 'Intuitive', 'message_body': "Dear {{firstname}}, \n\nYou are welcome"},
        {'id':2, 'client_id': 1, 'trans_channel_id': 2, 'noti_type_id': 2, 'sender_id': 'Intuitive', 'message_body': "Dear {{firstname}}, \n\nAn account just signed in"}
    ]
    if NotificationSample.noti_sample_object(db).count() == 0:
        noti_instance = [NotificationSample(**noti) for noti in noti_data]
        db.add_all(noti_instance)
        db.commit() 
        
def seed_transport_configuration(db: Session):
    from db.models import TransportConfiguration

    config_data = [
        {"client_id": 1, "trans_channel_id": 1, "trans_method": "smtp-email", "trans_config":
            {"mail_server": "smtp.gmail.com", "mail_username": "Intuitive",
             "mail_password": "heeiovmgrudlmtvi", "smtp_port": 567,
             "mail_tls": True, "mail_ssl": False}},
        {"client_id": 1, "trans_channel_id": 2, "trans_method": "twilio-sms", "trans_config":
            {"account_sid": "3ewfsrdsvehs", "auth_token": "er34ttedgu34ug",
             "sender_number": "8085463728"}},
        {"client_id": 1, "trans_channel_id": 2, "trans_method": "nexmo-sms", "trans_config":
            {"api_key": "3ewfsrdsvehs", "secret_key": "er34ttedgu34ug",
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
        {'client_id': 1, 'trans_channel_id': 2, 'trans_config_id': 3}
    ]
    
    if ActiveChannelClientConfig.active_channel_client_object(db).count() == 0:
        active_instance = [ActiveChannelClientConfig(**config) for  config in active_config]
        db.add_all(active_instance)
        db.commit()
     
def seed_noti_history(db: Session):
    from db.models import NotificationHistory
    
    noti_hist_data = [
        {'id':1, 'client_id':1, 'trans_channel_id':1, 'noti_type_id': 1, 'message_body':'Dear User, <br> You are testing email',
         'subject':'Testing Email', 'sender_email': 'abc@gmail.com', 'sender_id': 'Intuitive test',
         'recipients': ['abcd@gmail.comm']},
        {'id':2, 'client_id':1, 'trans_channel_id':2, 'noti_type_id': 1, 'message_body':'Dear User, <br> You are testing sms',
         'subject':'Testing SMS', 'sender_id': 'Intuitive test',
         'recipients': ['234']
        }
    ]  
    
    if NotificationHistory.notification_history_object(db).count() == 0:
        active_instance = [NotificationHistory(**noti) for  noti in noti_hist_data]
        db.add_all(active_instance)
        db.commit()
        
def seed_notification_variable(db: Session):
    from db.models import NotificationVariables
    
    noti_variable_data = [
        {'id': 1, 'noti_type': 'login', 'noti_variable': [1, 2, 5, 6, 10, 8, 9, 7]},
        {'id': 2, 'noti_type':'welcome', 'noti_variable': [1, 5, 2, 6, 8, 9, 7]},
        {'id': 3, 'noti_type':'forget-password', 'noti_variable': [1, 5, 2, 11, 6, 7]},
        {'id': 4, 'noti_type': 'reset-password', 'noti_variable': [2, 1, 4, 12, 5, 6, 7]},
        {'id': 5, 'noti_type': 'registeration', 'noti_variable': [2, 5, 4, 3, 6, 7]}
    ]
    
    if NotificationVariables.notification_variable_object(db).count() == 0:
        active_instance = [NotificationVariables(**noti) for  noti in noti_variable_data]
        db.add_all(active_instance)
        db.commit()
        
def seed_parent_variables(db: Session):
    from db.models import ParentVariables
    
    parent_variable = [
        {'id': 1, 'variable_text': 'username', 'replace_text': '{{username}}'},
        {'id': 2, 'variable_text': 'first_name', 'replace_text': '{{first_name}}'},
        {'id': 3, 'variable_text': 'password', 'replace_text': '{{password}}'},
        {'id': 4, 'variable_text': 'login_url', 'replace_text': '{{login_url}}'},
        {'id': 5, 'variable_text': 'email_address', 'replace_text': '{{email_address}}'},
        {'id': 6, 'variable_text': 'phone_number', 'replace_text': '{{phone_number}}'},
        {'id': 7, 'variable_text': 'company_name', 'replace_text': '{{company_name}}'},
        {'id': 8, 'variable_text': 'date', 'replace_text': '{{date}}'},
        {'id': 9, 'variable_text': 'time', 'replace_text': '{{time}}'},
        {'id': 10, 'variable_text': 'ip_address', 'replace_text': '{{ip_address}}'},
        {'id': 11, 'variable_text': 'reset_url', 'replace_text': '{{reset_url}}'},
        {'id': 12, 'variable_text': 'new_password', 'replace_text': '{{new_password}}'},
    ]
    
    if ParentVariables.parent_variable_object(db).count() == 0:
        active_instance = [ParentVariables(**parent) for  parent in parent_variable]
        db.add_all(active_instance)
        db.commit()