from .conftest import get_session
import sys
sys.path.append("..")
from db import models
from schema import ClientSchema
import uuid

def test_client_crud(get_session):
    # data to populate the table with.
    client_data = {
        'slug': 'client-A',
        'client_key': str(uuid.uuid4())
    }
    
    # first check that table is empty.
    retrieve_clients = models.Client.retrieve_client(get_session)
    assert len(retrieve_clients) == 0
    # create a client (CREATE AND RETRIEVE)
    client = ClientSchema(**client_data)
    created_client = models.Client.create_client(get_session, client.slug, client.client_key)
    get_session.add(created_client)
    get_session.commit()
    
    assert created_client is not None
    # ensure it was created.
    retrieve_clients = models.Client.retrieve_client(get_session)
    assert len(retrieve_clients) == 1
    
    # get the client details, and also check that the attributes exists.
    get_details = models.Client.check_key(get_session, client.client_key)
    assert get_details.slug == client.slug
    assert get_details.client_key == client.client_key
    assert get_details.status == True
    assert get_details.created_at is not None
    assert get_details.updated_at is not None
    
    # update.(SLOW DELETE)
    get_details.status = False
    get_session.commit()
    
    #retrieve after update.
    get_updated_details = models.Client.check_key(get_session, client.client_key)
    assert get_updated_details.status == False
    
    

def test_client_queries(get_session):
    client_data_1 = {
        'slug': 'client-A',
        'client_key': str(uuid.uuid4())
    }
    
    client_data_2 = {
        'slug': 'client-B',
        'client_key': str(uuid.uuid4())
    }
    
    client_1 = ClientSchema(**client_data_1)
    created_client_1 = models.Client.create_client(get_session, client_1.slug, client_1.client_key)
    get_session.add(created_client_1)
    get_session.commit()
       
    retrieve_client = models.Client.retrieve_client(get_session)
    
    assert len(retrieve_client) == 1
    
    # check if key exists or not
    # Here does not exists.
    check_key_1 = models.Client.check_key(get_session, str(uuid.uuid4()))
    assert check_key_1 is None
    # Here Key exists.
    check_key_2 = models.Client.check_key(get_session, client_1.client_key)
    assert check_key_2 is not None



    
    
    
    
    
    
    