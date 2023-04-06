# Schemas
from pydantic import BaseModel as PydanticBaseModel
from pydantic import validator, EmailStr, Field
from typing import List, Optional, Dict, Union


class BaseModel(PydanticBaseModel):
    class config:
        orm_mode = True

class ClientSchema(BaseModel):
    slug: str
    client_key: str   
    
class UpdateStatusSchema(BaseModel):
    status: bool
    
    @validator('status')
    def validate_status(cls, v):
        if v not in (True, False):
            raise ValueError("Value must be True or False")
        return v
            
class UpdateClientKeySchema(BaseModel):
    client_key: str
    
class NotificationDataSchema(BaseModel):
    client_id: int
    trans_channel_id: int
    noti_type_id: int
    message_body: str
    subject: str = Field(None, max_length=100) 
    sender_id: str
    sender_email: EmailStr = None
    carbon_copy: Optional[List[EmailStr]] = None
    blind_copy: Optional[List[EmailStr]] = None
    
class NotificationUpdateSchema(BaseModel):
    message_body: str = None
    subject: str = Field(None, max_length=100)
    sender_id: str = None
    sender_email: EmailStr = None
    carbon_copy: Optional[List[EmailStr]] = None
    blind_copy: Optional[List[EmailStr]] = None
    notification_state: bool = None
    
    @validator('notification_state')
    def validate_notification_state(cls, v):
        if v not in (True, False):
            raise ValueError("Value must be True or False")
        return v
    
class TransportConfigSchema(BaseModel):
    client_id: int
    trans_channel_id: int
    trans_method: str
    trans_config: Dict[str, Union[bool, int, str]]
    
class TransportConfigUpdateSchema(BaseModel):
    trans_config: Optional[Dict[str, Union[bool, int, str]]] = None
    transport_state: bool =None
    
    @validator('transport_state')
    def validate_transport_state(cls, v):
        if v not in (True, False):
            raise ValueError("Value must be True or False")
        return v

    