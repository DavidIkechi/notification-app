from .conftest import get_session
import sys
sys.path.append("..")
from db import models
from schema import ClientSchema, UpdateStatusSchema
import uuid

def test_client_model(get_session):
    # data to populate the table with.
    client_data = {
        'slug': 'client-A',
        'client_key': str(uuid.uuid4())
    } 
    # first check that table is empty.
    retrieve_clients = models.Client.retrieve_all_client(get_session)
    assert len(retrieve_clients) == 0
    # create a client (CREATE AND RETRIEVE)
    client = ClientSchema(**client_data)
    created_client = models.Client(slug=client.slug, client_key=client.client_key)
    get_session.add(created_client)
    get_session.commit()
    
    assert created_client is not None
    # ensure it was created.
    retrieve_clients = models.Client.retrieve_all_client(get_session)
    assert len(retrieve_clients) == 1
    
# To test if the static create client method actually adds record to the client table.
def test_add_client(get_session):
    # data to populate the table with.
    client_data = {
        'slug': 'client-A',
        'client_key': str(uuid.uuid4())
    } 
    # first check if the client table is empty.
    retrieve_clients = models.Client.retrieve_all_client(get_session)
    assert len(retrieve_clients) == 0
    
    # add the data.
    client = ClientSchema(**client_data)
    created_client = models.Client(slug=client.slug, client_key=client.client_key)
    get_session.add(created_client)
    get_session.commit()
    
    # check if the record was inserted.
    retrieve_all_records = models.Client.retrieve_all_client(get_session)
    assert len(retrieve_all_records) == 1
    
    # get the client details, and also check that the attributes inserted has proper values.
    get_details = models.Client.check_single_key(get_session, client.client_key)
    assert get_details.slug == client.slug
    assert get_details.client_key == client.client_key
    assert get_details.status == True
    assert get_details.created_at is not None
    assert get_details.updated_at is not None

def test_client_key_exists(get_session):
    client_data_1 = {
        'slug': 'client-A',
        'client_key': str(uuid.uuid4())
    }
    
    client_1 = ClientSchema(**client_data_1)
    created_client_1 = models.Client.create_single_client(get_session, client_1.slug, client_1.client_key)
    get_session.add(created_client_1)
    get_session.commit()
      
    # check that the client was inserted and only record exists in the table. 
    retrieve_client = models.Client.retrieve_all_client(get_session)
    assert len(retrieve_client) == 1
    
    # check if the key exsts
    check_key = models.Client.check_single_key(get_session, client_1.client_key)
    assert check_key is not None
    
    
def test_client_key_not_exists(get_session):
    # first check that table is empty.
    retrieve_clients = models.Client.retrieve_all_client(get_session)
    assert len(retrieve_clients) == 0
    # key does not exists
    check_key = models.Client.check_single_key(get_session, str(uuid.uuid4()))
    assert check_key is None
    

def test_update_client_status(get_session):
    client_data_1 = {
        'slug': 'client-A',
        'client_key': str(uuid.uuid4())
    }
    
    client_1 = ClientSchema(**client_data_1)
    created_client_1 = models.Client.create_single_client(get_session, client_1.slug, client_1.client_key)
    get_session.add(created_client_1)
    get_session.commit()
    
    get_details = models.Client.check_single_key(get_session, client_1.client_key)
    assert get_details.slug == client_1.slug
    assert get_details.client_key == client_1.client_key
    assert get_details.status == True
    
    # update the status
    update_data = {
        'status': False
    }
    
    client_update_data = UpdateStatusSchema(**update_data)
    updated_client = models.Client.update_single_client(
        get_session, get_details.id, client_update_data.dict(exclude_unset=True))
    get_session.commit()
    get_session.refresh(updated_client)
    
    # check that the client is updated to False
    get_details = models.Client.check_single_key(get_session, client_1.client_key)
    assert get_details.slug == client_1.slug
    assert get_details.client_key == client_1.client_key
    assert get_details.status == False
    
    
    

    
    
    
    
    
    
    