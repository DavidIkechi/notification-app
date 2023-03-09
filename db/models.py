# for models.
from .session import Base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.orm import Session
import uuid
from datetime import datetime
from sqlalchemy.sql import text
class Client(Base):
    __tablename__ = "client"
    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    client_key = Column(String(250), unique=True, nullable=False, index=True)
    status = Column(Boolean, default=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        default = datetime.utcnow(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=datetime.utcnow(), 
                        onupdate=datetime.utcnow(), nullable=False)
    
    # static method to check if the key exists
    @staticmethod
    def check_single_key(db: Session, client_key):
        return db.query(Client).filter_by(client_key = client_key).first()
    
    # static method to create client.   
    @staticmethod
    def create_single_client(db: Session, slug, client_key):
        return Client(slug = slug, client_key = client_key)  
    
    @staticmethod
    def retrieve_all_client(db: Session):
        return db.query(Client).all()
    
    @staticmethod
    def update_single_client(db: Session, client_key, client_data):
        return (
            db.query(Client).filter_by(client_key = client_key).update(client_data) 
            and db.query(Client).filter_by(client_key=client_key).first() 
            or None
        )
    
            
            
        
    
    
    
    
    