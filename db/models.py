# for models.
from .session import Base
from sqlalchemy import Column, Enum, Integer, String, Boolean, TIMESTAMP, ForeignKey, Float, JSON, TEXT
from sqlalchemy.orm import Session, load_only, relationship
import uuid
from datetime import datetime
from sqlalchemy.sql import text
import sys
sys.path.append("..")


# Client Table.
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
    # relationship
    noti_sample = relationship('NotificationSample', back_populates='client')
    trans_config = relationship('TransportConfiguration', back_populates='client')
    active_channel_config = relationship('ActiveChannelClientConfig', back_populates='client')
    noti_history = relationship('NotificationHistory', back_populates='client')
    # get the client object
    @staticmethod
    def get_client_object(db: Session):
        return db.query(Client)
                               
    # get the client by ID
    @staticmethod
    def get_client_by_id(db: Session, id: int):
        return Client.get_client_object(db).get(id)
        
    # static method to check if the key exists
    @staticmethod
    def check_single_key(db: Session, client_key):
        return Client.get_client_object(db).filter_by(client_key = client_key).first()
    
    # static method to create client.   
    @staticmethod
    def create_single_client(db: Session, slug, client_key):
        return Client(slug = slug, client_key = client_key)  
    
    @staticmethod
    def retrieve_all_client(db: Session):
        return Client.get_client_object(db).options(load_only(Client.slug, Client.status)).all()
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
    # static method
    @staticmethod
    def update_single_client(db: Session, client_id, client_data): 
        client = Client.get_client_by_id(db, client_id)
        for key, value in client_data.items():
            setattr(client, key, value)
        return client

# Transport Channel Table    
class TransportChannel(Base):
    __tablename__ = 'transport_channel'
    id = Column(Integer, primary_key=True, index=True)
    channel_type = Column(String(255), nullable= False, unique=True, index=True)    
    slug = Column(String(100), unique=True, nullable=False, index=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        default = datetime.utcnow(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=datetime.utcnow(), 
                        onupdate=datetime.utcnow(), nullable=False)
    # relationship.
    noti_sample = relationship('NotificationSample', back_populates='trans_channel')
    channel_trans = relationship('ChannelTransportType', back_populates='trans_channel')
    trans_config = relationship('TransportConfiguration', back_populates='trans_channel')
    active_channel_config = relationship('ActiveChannelClientConfig', back_populates='trans_channel')
    noti_history = relationship('NotificationHistory', back_populates='trans_channel')
    # start defining the static methods.
    @staticmethod
    def get_transport_channel_object(db: Session):
        return db.query(TransportChannel)
    
    @staticmethod
    def get_channel_by_id(db: Session, channel_id):
        return TransportChannel.get_transport_channel_object(db).get(channel_id)
    
    @staticmethod
    def get_channel_by_slug(db: Session, slug_name):
        return TransportChannel.get_transport_channel_object(db).filter_by(
            slug = slug_name).first()
    
    @staticmethod
    def retrieve_channels(db: Session):
        return TransportChannel.get_transport_channel_object(db).all()

# Notification Type Table   
class NotificationType(Base):
    __tablename__ = 'notification_type'
    id = Column(Integer, primary_key=True, index=True)
    noti_type = Column(String(255), nullable=False, index=True)
    slug = Column(String(100), unique=True, nullable=False, index=True)

    created_at = Column(TIMESTAMP(timezone=True),
                        default = datetime.utcnow(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=datetime.utcnow(), 
                        onupdate=datetime.utcnow(), nullable=False)
    # relationships.
    noti_sample = relationship('NotificationSample', back_populates='noti_type')
    noti_history = relationship('NotificationHistory', back_populates='noti_type')

    # start defining the static methods.
    @staticmethod
    def get_notification_object(db: Session):
        return db.query(NotificationType)
    
    @staticmethod
    def retrieve_notification_types(db: Session):
        return NotificationType.get_notification_object(db).all()
    
    @staticmethod
    def get_notification_by_id(db: Session, noti_id: int):
        return NotificationType.get_notification_object(db).get(noti_id)
    
    @staticmethod
    def get_notification_by_slug(db: Session, slug: str):
        return NotificationType.get_notification_object(db).filter_by(
            slug = slug
        ).first()

# Notification Sample Table     
class NotificationSample(Base):
    __tablename__ = 'notification_sample'
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey('client.id', ondelete='CASCADE'))
    trans_channel_id = Column(Integer, ForeignKey('transport_channel.id', ondelete='CASCADE'))
    noti_type_id = Column(Integer, ForeignKey('notification_type.id', ondelete='CASCADE'))
    message_body = Column(TEXT, nullable=False)
    subject = Column(String(100), nullable=True) # plus spaces.
    sender_id = Column(String(255), nullable=False)
    sender_email = Column(String(255), nullable=True)
    carbon_copy = Column(JSON, nullable=True, default=[])
    blind_copy = Column(JSON, nullable=True, default=[])
    notification_state = Column(Boolean, default= False) # default should be false.
    # creating the relationship for the foreign keys.
    client = relationship('Client', back_populates='noti_sample')
    trans_channel = relationship('TransportChannel', back_populates='noti_sample')
    noti_type = relationship('NotificationType', back_populates='noti_sample')
    # created and updated at.
    created_at = Column(TIMESTAMP(timezone=True),
                        default = datetime.utcnow(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=datetime.utcnow(), 
                        onupdate=datetime.utcnow(), nullable=False)
    #static methods.
    @staticmethod
    def noti_sample_object(db: Session):
        return db.query(NotificationSample)
    
    @staticmethod
    def get_noti_sample_by_id(db: Session, noti_id):
        return NotificationSample.noti_sample_object(db).get(noti_id)
    
    @staticmethod
    def create_noti_sample(db: Session, noti_data: dict):
        return NotificationSample(**noti_data)
    
    @staticmethod
    def update_noti_sample(db: Session, noti_id, noti_update_data: dict):
        noti_sample = NotificationSample.get_noti_sample_by_id(db, noti_id)
        for key, value in noti_update_data.items():
            setattr(noti_sample, key, value)
        return noti_sample 
    
    @staticmethod
    def retrieve_noti_samples_by_status(db:Session, client_id, noti_status):
        return NotificationSample.noti_sample_object(db).filter_by(
            client_id = client_id, notification_state = noti_status
        )
    
    @staticmethod
    def retrieve_noti_samples_by_trans_channel(db: Session, client_id, channel_id):
        return NotificationSample.noti_sample_object(db).filter_by(
            client_id = client_id, trans_channel_id = channel_id
        )
        
    @staticmethod
    def retrieve_all_noti_samples_by_client_id(db: Session, client_id):
        return NotificationSample.noti_sample_object(db).filter_by(
            client_id = client_id)
        
    @staticmethod
    def check_noti_sample_by_noti_type(db: Session, client_id, noti_type_id):
        return NotificationSample.noti_sample_object(db).filter_by(
            client_id = client_id, noti_type_id = noti_type_id
        )
    
    @staticmethod
    def check_noti_sample_by_noti_type_tran(db: Session, client_id, noti_type_id, channel_id):
        return NotificationSample.noti_sample_object(db).filter_by(
            client_id = client_id, noti_type_id = noti_type_id, trans_channel_id = channel_id
        ).first()
        
    @staticmethod
    def retrieve_noti_samples(db: Session):
        return NotificationSample.noti_sample_object(db).all()
        
# Channel Transport Type
class ChannelTransportType(Base):
    __tablename__ = 'channel_transport_type'
    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(Integer, ForeignKey('transport_channel.id', ondelete='CASCADE'))
    parameters = Column(JSON, nullable=False)
    gate_way = Column(String(255), nullable=False, unique=True)
    slug = Column(String(100), unique=True, nullable=False, index=True)

    
    trans_channel = relationship('TransportChannel', back_populates='channel_trans')
    # created and updated at.
    created_at = Column(TIMESTAMP(timezone=True),
                        default = datetime.utcnow(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=datetime.utcnow(), 
                        onupdate=datetime.utcnow(), nullable=False)
    
    #static methods
    @staticmethod
    def get_channel_transport_object(db: Session):
        return db.query(ChannelTransportType)
    
    @staticmethod
    def retrieve_gateways(db: Session):
        return ChannelTransportType.get_channel_transport_object(db).options(load_only(
            ChannelTransportType.channel_id, ChannelTransportType.gate_way
        )).all()
        
    @staticmethod
    def get_channel_trans_params_by_id(db: Session, gateway_id: int):
        return ChannelTransportType.get_channel_transport_object(db).get(gateway_id)
    
    @staticmethod
    def get_channel_trans_param_by_slug(db: Session, gateway_slug: str):
        return ChannelTransportType.get_channel_transport_object(db).filter_by(
            slug = gateway_slug).first()
        
        
class TransportConfiguration(Base):
    __tablename__ =  "transport_configuration"
    id = Column(Integer, primary_key=True, index = True)
    client_id = Column(Integer, ForeignKey('client.id', ondelete='CASCADE'))
    trans_channel_id = Column(Integer, ForeignKey('transport_channel.id', ondelete='CASCADE'))
    trans_method = Column(String(255), ForeignKey('channel_transport_type.slug'), index = True, nullable=False)
    trans_config = Column(JSON, nullable=False)
    transport_state = Column(Boolean, default=True)
    # created and updated at.
    created_at = Column(TIMESTAMP(timezone=True),
                        default = datetime.utcnow(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=datetime.utcnow(), 
                        onupdate=datetime.utcnow(), nullable=False)
    # creating the relationship.
    client = relationship('Client', back_populates='trans_config')
    trans_channel = relationship('TransportChannel', back_populates='trans_config')
    active_channel_config = relationship('ActiveChannelClientConfig', back_populates='trans_config')
    # creating static methods.
    @staticmethod
    def transport_config_object(db: Session):
        return db.query(TransportConfiguration)
    
    @staticmethod
    def create_transport_config(db: Session, trans_config_data: dict):
        return TransportConfiguration(**trans_config_data)
    
    @staticmethod
    def update_transport_config(db: Session, config_id, config_update_data: dict):
        trans_conf = TransportConfiguration.get_transport_config_by_id(db, config_id)
        for key, value in config_update_data.items():
            setattr(trans_conf, key, value)
        return trans_conf
        
    @staticmethod
    def get_transport_config_by_id(db: Session, config_id):
        return TransportConfiguration.transport_config_object(db).get(config_id)
    
    @staticmethod
    def get_transport_config_by_method(db: Session, client_id, trans_method):
        return TransportConfiguration.transport_config_object(db).filter_by(
            client_id = client_id, trans_method = trans_method   
        ).first()
    
    @staticmethod    
    def get_transport_config_by_trans_state(db: Session, client_id, trans_state):
        return TransportConfiguration.transport_config_object(db).filter_by(
            client_id = client_id, transport_state = trans_state   
        )
        
    @staticmethod
    def get_transport_cconfig_by_channel_id(db: Session, client_id, channel_id):
        return TransportConfiguration.transport_config_object(db).filter_by(
            client_id = client_id, trans_channel_id=channel_id
        )
    
    @staticmethod
    def get_transport_configs_by_client_id(db: Session, client_id):
        return TransportConfiguration.transport_config_object(db).filter_by(
            client_id=client_id)
        
    @staticmethod
    def retrieve_transport_configs(db: Session):
        return TransportConfiguration.transport_config_object(db)
    

class ActiveChannelClientConfig(Base):
    __tablename__ = "active_channel_client_config"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey('client.id', ondelete='CASCADE'))
    trans_channel_id = Column(Integer, ForeignKey('transport_channel.id', ondelete='CASCADE'))
    trans_config_id = Column(Integer, ForeignKey('transport_configuration.id', ondelete='CASCADE'))
    # created and updated at.
    created_at = Column(TIMESTAMP(timezone=True),
                        default = datetime.utcnow(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=datetime.utcnow(), 
                        onupdate=datetime.utcnow(), nullable=False)
    # relationships
    client = relationship('Client', back_populates='active_channel_config')
    trans_channel = relationship('TransportChannel', back_populates='active_channel_config')
    trans_config = relationship('TransportConfiguration', back_populates='active_channel_config')
    
    # static methods.
    @staticmethod
    def active_channel_client_object(db: Session):
        return db.query(ActiveChannelClientConfig)
    
    @staticmethod
    def get_active_channel_by_id(db: Session, active_id: int):
        return ActiveChannelClientConfig.active_channel_client_object(db).get(active_id)
    
    @staticmethod
    def get_active_channel_by_client_id(db: Session, client_id: int):
        return ActiveChannelClientConfig.active_channel_client_object(db).filter_by(
            client_id = client_id).all()
        
    @staticmethod
    def get_active_channel_by_trans_config_id(db: Session, trans_config_id: int):
        return ActiveChannelClientConfig.active_channel_client_object(db).filter_by(
            trans_config_id = trans_config_id).first()
    
    @staticmethod
    def retrieve_active_channels(db: Session):
        return ActiveChannelClientConfig.active_channel_client_object(db)
    
    @staticmethod
    def retrieve_active_channels_by_trans_channel(db: Session, trans_channel_id: int):
        return ActiveChannelClientConfig.active_channel_client_object(db).filter_by(
            trans_channel_id = trans_channel_id)
    
    @staticmethod
    def get_active_channel_by_client_tran_id(db: Session, client_id: int, trans_channel_id: int):
        return ActiveChannelClientConfig.active_channel_client_object(db).filter_by(
            client_id= client_id, trans_channel_id= trans_channel_id)
        
    @staticmethod
    def create_active_channel(db: Session, active_client_data: dict):
        return ActiveChannelClientConfig(**active_client_data)
    
    @staticmethod
    def update_active_channel(db: Session, active_id, active_update_data: dict):
        active_conf = ActiveChannelClientConfig.get_active_channel_by_id(db, active_id)
        for key, value in active_update_data.items():
            setattr(active_conf, key, value)
        return active_conf
        

class NotificationHistory(Base):
    __tablename__="notification_history"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey('client.id', ondelete='CASCADE'))
    trans_channel_id = Column(Integer, ForeignKey('transport_channel.id', ondelete='CASCADE'))
    noti_type_id = Column(Integer, ForeignKey('notification_type.id', ondelete='CASCADE'))
    message_body = Column(TEXT, nullable=False)
    subject = Column(String(100), nullable=True) # plus spaces.
    sender_id = Column(String(255), nullable=False)
    sender_email = Column(String(255), nullable=True)
    carbon_copy = Column(JSON, nullable=True, default=[])
    blind_copy = Column(JSON, nullable=True, default=[])
    recipients= Column(JSON, nullable=False)

    # when it was sent.
    message_id = Column(String(255), nullable=True, unique=True)
    sent_at = Column(TIMESTAMP(timezone=True),nullable=True)
    status = Column(String(100), nullable=False, default = "QUEUED")
    message_status = Column(String(255), nullable=True)
    scheduled_at = Column(TIMESTAMP(timezone=True),
                          default = datetime.utcnow(), nullable=False)
    # creating the relationship for the foreign keys.
    client = relationship('Client', back_populates='noti_history')
    trans_channel = relationship('TransportChannel', back_populates='noti_history')
    noti_type = relationship('NotificationType', back_populates='noti_history')
    # created and updated at.
    created_at = Column(TIMESTAMP(timezone=True),
                        default = datetime.utcnow(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=datetime.utcnow(), 
                        onupdate=datetime.utcnow(), nullable=False)
    
    # start creating the static methods
    @staticmethod
    def notification_history_object(db: Session):
        return db.query(NotificationHistory)
    
    @staticmethod
    def create_notification_history(db: Session, noti_history_data: dict):
        return NotificationHistory(**noti_history_data)
    
    @staticmethod
    def get_noti_history_by_id(db: Session, history_id):
        return NotificationHistory.notification_history_object(db).get(history_id)
    
    @staticmethod
    def update_notification_history(db: Session, history_id, noti_update_data: dict):
        noti_history = NotificationHistory.get_noti_history_by_id(db, history_id)
        for key, value in noti_update_data.items():
            setattr(noti_history, key, value)
        return noti_history
    
    @staticmethod
    def retrieve_noti_histories(db: Session):
        return NotificationHistory.notification_history_object(db)
    
class NotificationVariables(Base):
    __tablename__ = "notification_variables"
    id = Column(Integer, primary_key=True, index=True)
    noti_type = Column(String(100), ForeignKey('notification_type.slug', ondelete='CASCADE'), unique=True)
    noti_variable = Column(JSON, nullable=False)
        
    # created and updated at.
    created_at = Column(TIMESTAMP(timezone=True),
                        default = datetime.utcnow(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=datetime.utcnow(), 
                        onupdate=datetime.utcnow(), nullable=False)
    
    # static methods
    @staticmethod
    def notification_variable_object(db: Session):
        return db.query(NotificationVariables)
    
    @staticmethod
    def get_notification_variable_by_slug(db: Session, noti_type: str):
        return NotificationVariables.notification_variable_object(
            db).filter_by(noti_type = noti_type).first()
        
    @staticmethod
    def retrieve_notification_variables(db: Session):
        return NotificationVariables.notification_variable_object(db).all()
    
class ParentVariables(Base):
    __tablename__ = 'parent_variables'
    id = Column(Integer, primary_key=True, index=True)
    variable_text = Column(String(100), nullable=False, unique=True)
    replace_text = Column(String(100), nullable=False, unique=True)
    
    # created and updated at.
    created_at = Column(TIMESTAMP(timezone=True),
                        default = datetime.utcnow(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=datetime.utcnow(), 
                        onupdate=datetime.utcnow(), nullable=False)
    
    @staticmethod
    def parent_variable_object(db: Session):
        return db.query(ParentVariables)