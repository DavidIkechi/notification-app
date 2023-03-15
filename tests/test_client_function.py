from .conftest import get_session
import sys
sys.path.append("..")
from db import models
from schema import ClientSchema, UpdateStatusSchema, UpdateClientKeySchema
import uuid
from fastapi import status
from fastapi.testclient import TestClient
from apis.client import client_router
from main import notification_app


client_instance = TestClient(notification_app)

# create the client app instance.
def test_create_client(get_session):
    # data to populate the table with.
    client_data = {
        'slug': 'client-A',
        'client_key': str(uuid.uuid4())
    }
    # first check that table is empty.
    retrieve_clients = models.Client.retrieve_all_client(get_session)
    assert len(retrieve_clients) == 0
    # check root URL
    root_response = client_instance.get("/")
    assert root_response.status_code == status.HTTP_200_OK
    # get the client router
    client_response = client_instance.post("/clients/create_client", json=client_data)
    
    assert client_response.status_code == status.HTTP_201_CREATED
    assert client_response.json() == {"detail":"Client was successfully added"}
    # check the length of the table to be sure it has increased.
    retrieve_clients = models.Client.retrieve_all_client(get_session)
    assert len(retrieve_clients) == 1
    
# This function checks for error which occurs while creating the client  
def test_create_client_exist_error(get_session):
    # data to populate the table with.
    client_data = {
        'slug': 'client-A',
        'client_key': str(uuid.uuid4())
    }
    # first check that table is empty.
    retrieve_clients = models.Client.retrieve_all_client(get_session)
    assert len(retrieve_clients) == 0
    
    client = ClientSchema(**client_data)
    created_client = models.Client(slug=client.slug, client_key=client.client_key)
    get_session.add(created_client)
    get_session.commit()
    
    assert created_client is not None
    # ensure it was created.
    retrieve_clients = models.Client.retrieve_all_client(get_session)
    assert len(retrieve_clients) == 1
    
    # get the client router
    client_response = client_instance.post("/clients/create_client", json=client_data)
    
    assert client_response.status_code == 409
    assert client_response.json() == {"detail": "Client already exists"}
    

def test_create_client_insert_error(get_session):
    client_instance = TestClient(notification_app)
    # data to populate the table with.
    client_data = {
        'slug': None,
        'client_key': str(uuid.uuid4())
    }
    # first check that table is empty.
    retrieve_clients = models.Client.retrieve_all_client(get_session)
    assert len(retrieve_clients) == 0
    # unprocessiable entity error.
    client_response = client_instance.post("/clients/create_client", json=client_data)
    
    assert client_response.status_code == 422
    

def test_deactivate_client_with_middleware(get_session):
    # data to populate the table with.
    client_data = {
        'slug': 'client-A',
        'client_key': str(uuid.uuid4())
    }
    # first check that table is empty.
    retrieve_clients = models.Client.retrieve_all_client(get_session)
    assert len(retrieve_clients) == 0
    
    client = ClientSchema(**client_data)
    created_client = models.Client(slug=client.slug, client_key=client.client_key)
    get_session.add(created_client)
    get_session.commit()
    
    assert created_client is not None
    # ensure it was created.
    retrieve_clients = models.Client.retrieve_all_client(get_session)
    assert len(retrieve_clients) == 1
    # header.
    headers = {
        "Client-Authorization": client.client_key
    }
    # update the client status.
    client_response = client_instance.patch("/clients/deactivate_client", headers=headers)
    
    assert client_response.status_code == 200
    assert client_response.json() == {"detail":"Client was Successfully updated"}
    
    
def test_deactivate_client_without_middleware(get_session):
    # data to populate the table with.
    client_data = {
        'slug': 'client-A',
        'client_key': str(uuid.uuid4())
    }
    # first check that table is empty.
    retrieve_clients = models.Client.retrieve_all_client(get_session)
    assert len(retrieve_clients) == 0
    
    client = ClientSchema(**client_data)
    created_client = models.Client(slug=client.slug, client_key=client.client_key)
    get_session.add(created_client)
    get_session.commit()
    
    assert created_client is not None
    # ensure it was created.
    retrieve_clients = models.Client.retrieve_all_client(get_session)
    assert len(retrieve_clients) == 1
    # update the client status without headers
    client_response = client_instance.patch("/clients/deactivate_client")
    
    assert client_response.status_code == 401
    assert client_response.json() == {"detail":"Client key is missing"}
    

def test_update_client_key_with_middleware(get_session):
    # data to populate the table with.
    client_data = {
        'slug': 'client-A',
        'client_key': str(uuid.uuid4())
    }
    # first check that table is empty.
    retrieve_clients = models.Client.retrieve_all_client(get_session)
    assert len(retrieve_clients) == 0
    # schema
    client = ClientSchema(**client_data)
    client_response = client_instance.post("/clients/create_client", json=client_data)
    assert client_response.status_code == status.HTTP_201_CREATED
    
    retrieve_clients = models.Client.retrieve_all_client(get_session)
    assert len(retrieve_clients) == 1
    #get the key after inserting it into the database.
    # get the client details, and also check that the attributes inserted has proper values.
    get_details = models.Client.check_single_key(get_session, client.client_key)
    assert get_details.slug == client.slug
    assert get_details.client_key == client.client_key
    # header.
    headers = {
        "Client-Authorization": client.client_key
    }
    # update the key. 
    new_key = {
        'client_key':"new_key"
    }
    
    new_key_data = UpdateClientKeySchema(**new_key)
    client_response = client_instance.patch("/clients/update_client_key", json=new_key, headers=headers)
    
    assert client_response.status_code == 200
    assert client_response.json() == {"detail":"Client was Successfully updated"}

    # get the client details, and also check that the key change
    get_new_detail = models.Client.check_single_key(get_session, new_key_data.client_key)
    assert get_new_detail.slug == client.slug
    
    
    
    
    
 
    