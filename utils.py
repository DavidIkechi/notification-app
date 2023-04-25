from enum import Enum
from datetime import datetime
import re
import datetime as dt

# for adding utlity functions
def get_offset(page: int, page_size: int) -> int:
    return (page - 1) * page_size

# define the enum type for the status.
class Status(Enum):
    IN_PROGRESS = 'processing'
    SUCCESS = 'success'
    QUEUED = 'queue'
    FAILED = 'failed'
    
def exclude_none_values(data):
    """
    Helper function to exclude None values from a dictionary.
    """
    return {k: v for k, v in data.items() if v is not None}

def format_datetime(date_value):
    formatted_date = datetime.strptime(date_value, "%Y-%m-%dT%H:%M:%S.%fZ")
    # Format the datetime object as a string without the T and Z characters
    return formatted_date.strftime("%Y-%m-%d %H:%M:%S.%f")


def format_text(body_text: str, data: dict):
    # replace new lines with line breaks, to look like html texts.
    body_text = body_text.replace('\n', '<br>')
    # start formatting.
    placeholders = re.findall(r'{{(.*?)}}', body_text)

    # Replace placeholders with values from the dictionary
    formatted_text = body_text
    for placeholder in placeholders:
        value = data.get(placeholder.strip(), '')
        formatted_text = formatted_text.replace('{{' + placeholder + '}}', str(value))
    
    return formatted_text


def get_noti_data(noti_sample, schedule_data: dict):
    mess_body = format_text(noti_sample.message_body, 
                            schedule_data.noti_variables)
    
    noti_data ={
        'client_id': noti_sample.client_id,
        'trans_channel_id': noti_sample.trans_channel_id,
        'noti_type_id': noti_sample.noti_type_id,
        'message_body': mess_body,
        'subject': noti_sample.subject,
        'sender_id': noti_sample.sender_id,
        'sender_email': noti_sample.sender_email,
        'carbon_copy': noti_sample.carbon_copy,
        'blind_copy': noti_sample.blind_copy,
        'scheduled_at': schedule_data.scheduled_at
    }
    
    return exclude_none_values(noti_data)
    
    
    
# # import pika

# # # Connect to RabbitMQ server
# # connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
# # channel = connection.channel()

# # # Declare a queue
# # channel.queue_declare(queue='my_queue')
# from celery import Celery

# celery_app = Celery(
#     "myapp",
#     broker="amqp://guest:guest@localhost:5672//",
#     backend="rpc://",
# )

# @celery_app.task
# def add(x, y):
#     return x + y
