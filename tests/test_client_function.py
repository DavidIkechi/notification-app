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
import logging


client_instance = TestClient(notification_app)
# Add this line to configure logging
logging.basicConfig(level=logging.DEBUG)

# create the client app instance.
def test_create_client(get_session):
    # data to populate the table with.
    client_data = {
        'slug': 'client-A',
        'client_key': str(uuid.uuid4())
    }
    # check root URL
    root_response = client_instance.get("/")
    assert root_response.status_code == status.HTTP_200_OK
    # get the client router
    client_response = client_instance.post("/client/create", json=client_data)
    
    assert client_response.status_code == 201
    assert client_response.json()['detail'] == "Client was successfully created"
    assert client_response.json()['status'] == 1
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
    
    client = ClientSchema(**client_data)
    created_client = models.Client(slug=client.slug, client_key=client.client_key)
    get_session.add(created_client)
    get_session.commit()
    
    assert created_client is not None
    # ensure it was created.
    retrieve_clients = models.Client.retrieve_all_client(get_session)
    assert len(retrieve_clients) == 1
    
    # get the client router
    client_response = client_instance.post("/client/create", json=client_data)
    
    assert client_response.status_code == 400
    assert client_response.json()['detail'] == "Opps!, Client already exists!"
    assert client_response.json()['status'] == 0
    

def test_create_client_insert_error(get_session):
    client_instance = TestClient(notification_app)
    # data to populate the table with.
    client_data = {
        'slug': None,
        'client_key': str(uuid.uuid4())
    }
    
    # unprocessiable entity error.
    client_response = client_instance.post("/client/create", json=client_data)
    
    assert client_response.status_code != 201
    

def test_deactivate_client_with_middleware(get_session):
    # data to populate the table with.
    client_data = {
        'slug': 'client-A',
        'client_key': str(uuid.uuid4())
    }
    
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
    client_response = client_instance.patch("/client/deactivate", headers=headers)
    
    assert client_response.status_code == 200
    assert client_response.json()['status'] == 1
    # check if it was deactivated.
    assert client_response.json()['detail']['status'] == False 


def test_deactivate_client_without_middleware(get_session):
    # data to populate the table with.
    client_data = {
        'slug': 'client-A',
        'client_key': str(uuid.uuid4())
    }
    
    client = ClientSchema(**client_data)
    created_client = models.Client(slug=client.slug, client_key=client.client_key)
    get_session.add(created_client)
    get_session.commit()
    
    assert created_client is not None
    # ensure it was created.
    retrieve_clients = models.Client.retrieve_all_client(get_session)
    assert len(retrieve_clients) == 1
    # update the client status without headers
    client_response = client_instance.patch("/client/deactivate")
    
    assert client_response.status_code == 401
    assert client_response.json() == {"detail":"Client key is missing"}
    

def test_update_client_key_with_middleware(get_session):
    # data to populate the table with.
    client_data = {
        'slug': 'client-A',
        'client_key': str(uuid.uuid4())
    }
    # synchronizing with the schemas.
    client = ClientSchema(**client_data)
    client_response = client_instance.post("/client/create", json=client_data)
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
    client_response = client_instance.patch("/client/update", json=new_key, headers=headers)
    assert client_response.status_code == 200
    # check if the key has been updated
    assert client_response.json()['detail']['client_key'] == new_key_data.client_key
    # chekck that the key is different from the old key.
    assert client_response.json()['detail']['client_key'] !=  client.client_key

 
def test_reactivate_client(get_session):
    # data to populate the table with.
    client_data = {
        'slug': 'client-A',
        'client_key': str(uuid.uuid4())
    }
    
    client = ClientSchema(**client_data)
    created_client = models.Client(slug=client.slug, client_key=client.client_key)
    get_session.add(created_client)
    get_session.commit()
    
    assert created_client is not None
    # ensure it was created.
    client_response = client_instance.patch(f"/client/reactivate/1")
    assert client_response.status_code == 200
    assert client_response.json()['detail']['status'] == True
    assert client_response.json()['status'] == 1
    
    
def test_reactivate_client_error(get_session):
    client_data = {
        'slug': 'client-A',
        'client_key': str(uuid.uuid4())
    }

    client = ClientSchema(**client_data)
    created_client = models.Client(slug=client.slug, client_key=client.client_key)
    get_session.add(created_client)
    get_session.commit()
    
    assert created_client is not None
    # ensure it was created.
    client_response = client_instance.patch("/client/reactivate/5")
    assert client_response.status_code == 400
    assert client_response.json()['detail'] == "Client with such id does not exists"
    assert client_response.json()['status'] == 0
    
def test_get_all_clients(get_session):
    
    client_data = {
        'slug': 'client-A',
        'client_key': str(uuid.uuid4())
    }
    
    client = ClientSchema(**client_data)
    created_client = models.Client(slug=client.slug, client_key=client.client_key)
    get_session.add(created_client)
    get_session.commit()
    
    client_data = {
        'slug': 'client-B',
        'client_key': str(uuid.uuid4())
    }
    
    client = ClientSchema(**client_data)
    created_client = models.Client(slug=client.slug, client_key=client.client_key)
    get_session.add(created_client)
    get_session.commit()
    # page 1 with 1 rcords per page
    client_response = client_instance.get("/client/", params={"page":1, "page_size":1})
    assert len(client_response.json()['data']['items'])== 1

    
    
    
    
    

    
    
    
 
    