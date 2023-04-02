from sqlalchemy.orm import Session
import sys
sys.path.append("..")
from db import models

# functions to populate models
def seed_transport(db: Session):
    # first check if the table is empty.
    transport_type = [
        {"id":1, "transport_type": "email"},
        {"id":2, "transport_type": "sms"}
    ]
    
    if models.TransportType.get_transport_object(db).count() == 0:
        transport_instance = [models.TransportType(**transport) for transport in transport_type]
        db.add_all(transport_instance)
        db.commit()
        
def seed_notification(db: Session):
    notification_type = [
        {"id": 1, "noti_type": "Login"},
        {"id": 2, "noti_type": "Forgot Password"},
        {"id": 3, "noti_type": "Reset Password"},
        {"id": 4, "noti_type": "Registeration"},
    ]
    
    if models.NotificationType.get_notification_object(db).count() == 0:
        notification_instance = [models.NotificationType(**notification) for notification in notification_type]
        db.add_all(notification_instance)
        db.commit()
        
        
        