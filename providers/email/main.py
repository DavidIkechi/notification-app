import sys
sys.path.append("..")
from abc import ABC, abstractmethod
from providers.email.smtp_mail import SMTPGateway
from providers.email.mailgun import MailGunGateway

# class EmailGateInterface(ABC):
#     @abstractmethod
#     def send_email(self, noti_data, trans_data):
#         pass


class EmailGate:
    def __init__(self, email_type, email_data):
        if email_type.lower() == "smtp-email":
            self.config = SMTPGateway(email_data)
        elif email_type.lower() == "mail-gun-email":
            self.config = MailGunGateway(email_data)
        else:
            self.config = None
    
    
    async def send_email(self, noti_data, trans_data):
        return await self.config.send_email(noti_data, trans_data)