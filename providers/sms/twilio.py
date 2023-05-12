from vonage import Client
import sys
sys.path.append("..")


class TwilioGateway:
    def __init__(self, sms_data):
        self.sms_config = Client(
            key=sms_data['account_sid'],
            secret=sms_data['auth_token']
        )
        
    async def send_sms(self, noti_data, trans_data):
        try:
            sms_result = {}
            response = self.sms_config.messages.create(
                to=noti_data['recipients'],
                from_=trans_data['sender_number'],
                body=noti_data['message_body']
            )
            
            if response.sid:
                sms_result['status'] = 'success'
                sms_result['message_id'] = response.sid
                sms_result['recipient_number'] = response.to
            else:
                sms_result['status'] = 'failed'
                sms_result['message_id'] = ''
                sms_result['recipient_number'] = noti_data['recipients']
            
        except Exception as e:
            raise Exception(f"An error occurred while sending the email: {e}")
        
        return sms_result