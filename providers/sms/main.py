import sys
sys.path.append("..")
from abc import ABC, abstractmethod
from providers.sms.nexmo import NexmoGateway
from providers.sms.twilio import TwilioGateway

class SMSGateInterface(ABC):
    @abstractmethod
    def send_sms(self, noti_data, trans_data):
        pass


class SMSGate(SMSGateInterface):
    def __init__(self, sms_type, sms_data):
        if sms_type.lower() == "nexmo-sms":
            self.config = NexmoGateway(sms_data)
        elif sms_type.lower() == "twilio-sms":
            self.config = TwilioGateway(sms_data)
        else:
            self.config = None
    
    
    async def send_sms(self, noti_data, trans_data):
        return await self.config.send_sms(noti_data, trans_data)