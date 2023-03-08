from .conftest import get_session
import sys
sys.path.append("..")
from db import models
from schema import ClientSchema
import uuid

def test_create_client(get_session):
    client_data = {
        'slug': 'client-A',
        'client_key': str(uuid.uuid4())
    }
    
    client = ClientSchema(**client_data)
    created_client = models.Client.create_client(get_session, client.slug, client.client_key)
    
    assert created_client.client_key == client.client_key
    assert created_client.slug == client.slug
    

def test_validate_key(get_session):
    client_data_1 = {
        'slug': 'client-A',
        'client_key': str(uuid.uuid4())
    }
    
    client_data_2 = {
        'slug': 'client-B',
        'client_key': "darfdv-12677w-ert"
    }
    
    client_1 = ClientSchema(**client_data_1)
    client_2 = ClientSchema(**client_data_2)
    
    validate_client_1 = models.Client.validate_key(client_1.client_key)
    validate_client_2 = models.Client.validate_key(client_2.client_key)
    
    assert validate_client_1 == True
    assert validate_client_2 == False
    

def test_retrieve_client(get_session):
    client_data_1 = {
        'slug': 'client-A',
        'client_key': str(uuid.uuid4())
    }
    
    client_data_2 = {
        'slug': 'client-B',
        'client_key': str(uuid.uuid4())
    }
    
    client_1 = ClientSchema(**client_data_1)
    client_2 = ClientSchema(**client_data_2)
    created_client_1 = models.Client.create_client(get_session, client_1.slug, client_1.client_key)
    created_client_2 = models.Client.create_client(get_session, client_2.slug, client_2.client_key)
    
    retrieve_client = models.Client.retrieve_client(get_session)
    
    assert len(retrieve_client) == 2
    
def test_delete_client(get_session):
    client_data_1 = {
        'slug': 'client-A',
        'client_key': str(uuid.uuid4())
    }
    
    client_data_2 = {
        'slug': 'client-B',
        'client_key': str(uuid.uuid4())
    }
    
    client_1 = ClientSchema(**client_data_1)
    client_2 = ClientSchema(**client_data_2)
    created_client_1 = models.Client.create_client(get_session, client_1.slug, client_1.client_key)
    created_client_2 = models.Client.create_client(get_session, client_2.slug, client_2.client_key)
    # retrieve the client.
    retrieve_client = models.Client.retrieve_client(get_session)
    # delete_client_1
    delete_client_1 = models.Client.delete_client(get_session, client_1.client_key)
    retrieve_client_1 = models.Client.retrieve_client(get_session)
    # delete client_2
    delete_client_2 = models.Client.delete_client(get_session, client_2.client_key)
    retrieve_client_2 = models.Client.retrieve_client(get_session)
    
    assert len(retrieve_client) == 2
    assert len(retrieve_client_1) == 1
    assert len(retrieve_client_2) == 0


    
    
    
    
    
    
    