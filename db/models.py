# for models.
from .session import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
import uuid

class Client(Base):
    __tablename__ = "client"
    id = Column(Integer, primary_key = True, index = True)
    slug = Column(String(100), nullable = False)
    client_key = Column(String(36), unique = True, nullable = False, index=True)
    
    # class method to validate the key.
    @classmethod
    def validate_key(cls, uuid_string):
        try:
            uuid_obj = uuid.UUID(uuid_string, version=4)
        except ValueError:
            return False
        return str(uuid_obj) == uuid_string
    
    # class method to check if the key exists
    @classmethod
    def check_key(cls, db: Session, client_key):
        check_key = db.query(cls).filter_by(client_key = client_key).first()
        if check_key:
            # it means user already exists.
            return True
        return False
    
    # class method to create client.   
    @classmethod
    def create_client(cls, db: Session, slug, client_key):
        # first check if the client_key exists.
        if cls.check_key(db, client_key) is False and cls.validate_key(client_key):
        # create the new client.
            new_cient = cls(slug = slug, client_key = client_key)
            db.add(new_cient)
            db.commit()
            
            return new_cient
        
        return None
    
    @classmethod
    def delete_client(cls, db: Session, client_key):
        # first check if the client key exists.
        if cls.check_key(db, client_key):
            remove_client = db.query(cls).filter_by(client_key = client_key).delete()
            db.commit()  
            return True
        return False
    
    @classmethod
    def retrieve_client(cls, db: Session):
        return db.query(cls).all()
    
            
            
        
    
    
    
    
    