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
        
        
        