from vonage import Client
import sys
sys.path.append("..")


class NexmoGateway:
    def __init__(self, sms_data):
        self.sms_config = Client(
            key=sms_data['api_key'],
            secret=sms_data['secret_key']
        )
        
    async def send_sms(self, noti_data, trans_data):
        try:
            sms_result = {}
            response = self.sms_config.sms.send_message(
                {
                    "from": trans_data['sender_number'],
                    "to": noti_data['recipients'],
                    "text": noti_data['message_body']
                }
            )
            
            if response["messages"][0]["status"] == "0":
                sms_result['status'] = 'success'
                sms_result['message_id'] = response["messages"][0]["message-id"]
                sms_result['recipient_number'] = response["messages"][0]["to"]
            else:
                sms_result['status'] = 'failed'
                sms_result['message_id'] = response["messages"][0]["error-text"]
                sms_result['recipient_number'] = noti_data['recipients']
            
        except Exception as e:
            raise Exception(f"An error occurred while sending the email: {e}")
        
        return sms_result