from enum import Enum
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
    
    
# import pika

# # Connect to RabbitMQ server
# connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
# channel = connection.channel()

# # Declare a queue
# channel.queue_declare(queue='my_queue')
from celery import Celery

celery_app = Celery(
    "myapp",
    broker="amqp://guest:guest@localhost:5672//",
    backend="rpc://",
)

@celery_app.task
def add(x, y):
    return x + y
