# Schemas
from pydantic import BaseModel as PydanticBaseModel
from pydantic import validator, EmailStr, Field
from typing import List, Optional, Dict, Union, Any
from datetime import datetime
from utils import format_datetime


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
    
class NotificationData(BaseModel):
    message_body: str
    subject: str = Field(None, max_length=100) 
    sender_id: str
    sender_email: EmailStr = None
    carbon_copy: Optional[List[EmailStr]] = None
    blind_copy: Optional[List[EmailStr]] = None
    
class NotificationDataSchema(NotificationData):
    client_id: int
    trans_channel_id: int
    noti_type_id: int
    
class NotificationDataEndpointSchema(NotificationData):
    client_slug: str
    trans_channel_slug: str
    noti_type_slug: str
    
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
    
class NotificationHistorySchema(BaseModel):
    scheduled_at: datetime = None
    noti_variables: Optional[Dict[str, Union[bool, int, str, List]]] = None
    recipients: List[str]
    noti_type_slug: str
    
    @validator('scheduled_at', pre=True, always=True)
    def format_scheduled_at(cls, value):
        return format_datetime(value) if value else None
    
class EmailSchema(BaseModel):
    body: Dict[str, Any]
    
class NotificationType(BaseModel):
    trans_type: str = None
    
class TransportConfigurationSchema(BaseModel):
    # trans channel can be sms or email
    trans_channel: str
    # trans_type can be smtp-email, nexmo
    trans_type: str
    trans_config: Dict[str, Union[bool, int, str]]