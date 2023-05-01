# all cron Jobs.
import sys
from sqlalchemy.orm import Session
sys.path.append("..")
from db import models
from crud.app_crud import update_noti_history

from datetime import datetime
from sqlalchemy import and_, or_, not_
from transport_config import (
    trans_configuration
)
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool, NullPool
from sqlalchemy import create_engine
# from db.session import Session as SessionLocal
from db.connection import get_db_conn_string
from db.session import engine, Session
import os
from celery_config import send_message
import json
from utils import exclude_none_values
from celery.result import AsyncResult


# This is called for the cron Job to observe new changes to database.
def initialized_db():    
    return Session()

def send_notification():
    # get all Jobs without rabbit id and with date less than now()
    db = initialized_db()
    try: 
        get_unsent_noti = (
            models.NotificationHistory.notification_history_object(db).filter(
                and_(
                    models.NotificationHistory.rabbit_id.is_(None),
                    models.NotificationHistory.scheduled_at <= datetime.utcnow(),
                    )).all()
            )
        
        for noti in get_unsent_noti:
            # get configuration info.
            config_data = models.ActiveChannelClientConfig.get_active_channel_by_client_tran_id(
                db, noti.client_id, noti.trans_channel_id).first()
            trans_type = config_data.trans_config.trans_method
            trans_data = config_data.trans_config.trans_config
            channel_type = config_data.trans_channel.slug
            trans_data['sender_id'] = noti.sender_id
            trans_data['sender_email'] = noti.sender_email
            noti_dict = noti.__dict__
            noti_dict.pop("_sa_instance_state")  # remove non-serializable data
            noti_dict.pop("scheduled_at")
            noti_dict.pop("updated_at")
            noti_dict.pop("created_at")
            noti_dict = exclude_none_values(noti_dict)
            # print(noti_dict)
            new_noti = noti_dict
            send_task = send_message.apply_async(args=[channel_type, trans_type, new_noti, trans_data])
            # update the data.
            cron_data = {
                "rabbit_id": str(send_task),
                "status": send_task.status
            }
            # print(db)
            result = update_noti_history(int(noti.id), cron_data)
    except Exception as e:
            print(f"An error occurred while sending the email: {e}")        
    
    
def update_notification():
    try:
        db = initialized_db()
        pushed_noti = (models.NotificationHistory.notification_history_object(db)
                       .filter(and_(models.NotificationHistory.rabbit_id.isnot(None),
                                    not_(or_(models.NotificationHistory.status == 'SUCCESS',
                                             models.NotificationHistory.status == 'FAILURE')
                                         )
                                    )
                               )
                       .all()
                       )
                
        for noti in pushed_noti:
            update_data = {}
            # get the id.
            task_id = noti.rabbit_id
            # check the status of things.
            result = AsyncResult(task_id)
            if result.ready():
                if result.successful():
                    get_message = result.result
                    message = get_message.get('result')
                    sent_at = get_message.get('completion_time')
                else:
                    error_data = result.info
                    if isinstance(error_data, Exception):
                        message = error_data.args[0].get('error_message')
                        sent_at = error_data.args[0].get('completion_time')
                # start populating.
                update_data['message_status'] = message
                update_data['sent_at'] = sent_at
            
            update_data['status'] = result.status
            result = update_noti_history(int(noti.id), update_data)
                 
    except Exception as e:
        print(f"An error occurred while sending the email: {e}")        

        