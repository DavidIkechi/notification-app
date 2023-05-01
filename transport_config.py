from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from fastapi.exceptions import HTTPException
from datetime import datetime, timedelta
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from schema import EmailSchema
import vonage
from twilio.rest import Client as twilio_client
from mailgun2 import Mailgun
from fastapi import BackgroundTasks

def trans_configuration(channel_type, trans_type, trans_data):
    if channel_type.lower() == "email":
        return email_configuration(trans_type, trans_data)
    elif channel_type.lower() == "sms":
        return sms_configuration(trans_type, trans_data)
    else:
        return None
    


def email_configuration(email_type, email_data):
    conf = None
    if email_type.lower() == "smtp-email":
        conf = ConnectionConfig(
            MAIL_USERNAME=email_data['sender_email'],
            MAIL_PASSWORD=email_data['mail_password'],
            MAIL_FROM=email_data['sender_email'],
            MAIL_PORT=int(email_data['smtp_port']),
            MAIL_SERVER=email_data['mail_server'],
            MAIL_FROM_NAME=email_data['mail_username'],
            MAIL_STARTTLS=email_data['mail_tls'],
            USE_CREDENTIALS=True,
            MAIL_SSL_TLS=email_data['mail_ssl'],
            VALIDATE_CERTS=True,
            TEMPLATE_FOLDER='./templates'
        )
    elif email_type.lower() == "mail-gun-email":
        conf = Mailgun(
            api_key=email_data['mail_api_key'], domain=email_data['mail_domain']
        )
        
    return conf 

def sms_configuration(sms_type, sms_data):
    client = None
    if sms_type.lower() == "nexmo-sms":
        client = vonage.Client(
            key=sms_data['api_key'], 
            secret=sms_data['secret_key'])
    
    elif sms_type.lower() == "twilio-sms":
        client = twilio_client(
            sms_data['account_sid'], sms_data['auth_token']
        )

    return client


async def send_email(transport_type, noti_data, config_object, trans_data):
    
    try:
        if transport_type.lower() == "smtp-email":
            background_tasks = BackgroundTasks()
            emails: EmailSchema = {
                "body": {
                    "text_body": noti_data['message_body']
                } 
            }
            
            message = MessageSchema(
                subject = noti_data['subject'],
                recipients = noti_data['recipients'],
                cc = noti_data['carbon_copy'],
                bcc = noti_data['blind_copy'],
                template_body=emails.get("body"),
                subtype=MessageType.html,
            )
            
            fm =FastMail(config_object)
            await fm.send_message(message=message, template_name='index.html')
            
        elif transport_type.lower() == "mail-gun-email":
            await mailgun.send_message(
                from_email="your-email@example.com",
                to_email=noti_data['recipients'],
                subject=noti_data['subject'],
                text=noti_data['message_body']
                )
    except Exception as e:
        print(f"An error occurred while sending the email: {e}") 
        
    return []

async def send_sms(transport_type, noti_data, config_object, trans_data):
    try:
        
        if transport_type.lower() == "nexmo-sms":
            await config_object.sms.send_message(
                {
                    "from": noti_data['sender_id'],
                    "to": noti_data['recipients'],
                    "text": noti_data['message_body'],
                }
            )
        
        elif transport_type.lower() == "twilio-sms":
            await config_object.messages.create(
                to=noti_data['recipients'],  # Replace with your recipient's phone number
                from_=trans_data['sender_number'],  # Replace with your Twilio phone number
                body=noti_data.message_body)
    
    except Exception as e:
        print(f"An error occurred while sending the email: {e}")   