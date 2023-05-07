from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
import sys
sys.path.append("..")
from schema import EmailSchema



class SMTPGateway:
    def __init__(self, email_data):
        self.email_config = ConnectionConfig(
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
        
    async def send_email(self, noti_data, trans_data):
        try:
            email_result = {}
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
            
            fm =FastMail(self.email_config)
            response = await fm.send_message(message=message, template_name='index.html')
            
            if response is not None:
                email_result['status'] = 'success'
                email_result['message'] = "Email was sent successfully"
                email_result['recipient_number'] = noti_data['recipients']
            else:
                email_result['status'] = 'failed'
                email_result['message_id'] = "Email was not sent"
                email_result['recipient_number'] = noti_data['recipients']
            
        except Exception as e:
            raise Exception(f"An error occurred while sending the email: {e}")
        
        return email_result