from celery import Celery, Task
# from transport_config import *
from fastapi import BackgroundTasks
import asyncio
from datetime import datetime
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
import sys
sys.path.append("..")
from providers.sms.main import SMSGate
from providers.email.main import EmailGate



celery_app = Celery(
    "noti_app",
    broker="amqp://guest:guest@localhost:5672//",
    backend="rpc://",
)
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],  
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

class MyCustomException(BaseException):
    def __init__(self, error_dict):
        self.error_dict = error_dict

@celery_app.task(track_started=True, bind=True)
def send_message(self, channel_type, transport_type, noti_data, trans_data):
    try: 
        if channel_type.lower() == "email":
            email_object = EmailGate(transport_type, trans_data)
            response = asyncio.run(email_object.send_email(noti_data, trans_data))
        elif channel_type.lower() == "sms":
            sms_object = SMSGate(transport_type, trans_data)
            response = asyncio.run(sms_object.send_sms(noti_data, trans_data))
        
        return {'result': 'Notification has been sent successfully', 
                'completion_time': datetime.utcnow()}
        
    except Exception as e:
        error_dict = {'error_message': str(e), 'completion_time': datetime.utcnow()}
        raise Exception(error_dict)
    
    
if __name__ == "__main__":
    # Run both applications
    celery_app.worker_main()