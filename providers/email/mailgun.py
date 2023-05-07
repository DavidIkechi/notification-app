from mailgun2 import Mailgun
import sys
sys.path.append("..")

class MailGunGateway:
    def __init__(self, email_data):
        self.email_config = Mailgun(
            api_key=email_data['mail_api_key'], domain=email_data['mail_domain']
        )
        
    async def send_email(self, noti_data, trans_data):
        try:
            response = self.email_config.send_message(
                from_email=trans_data['sender_email'],
                to_email=noti_data['recipients'],
                subject=noti_data['subject'],
                text=noti_data['message_body']
                )
            
            if response.status_code == 200:
                email_result['status'] = 'success'
                sms_result['message'] = "Email was sent successfuly"
                sms_result['recipient_number'] = noti_data['recipients']
            else:
                email_result['status'] = 'failed'
                email_result['message_id'] = "Email was not sent"
                email_result['recipient_number'] = noti_data['recipients']
            
        except Exception as e:
            raise Exception(f"An error occurred while sending the email: {e}")
        
        return email_result