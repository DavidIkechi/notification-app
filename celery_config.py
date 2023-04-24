from celery import Celery

celery_app = Celery(
    "notification_app",
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

@celery_app.task
def my_task(arg1, arg2):
    # do something
    pass

if __name__ == "__main__":
    # Run both applications
    celery_app.worker_main()