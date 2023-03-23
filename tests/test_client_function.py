from .conftest import get_session, client_instance
import sys
sys.path.append("..")
from db import models
from schema import ClientSchema, UpdateStatusSchema, UpdateClientKeySchema
import uuid
from fastapi import status
# from fastapi.testclient import TestClient
# from apis.client import client_router
# from main import notification_app
import logging


# Add this line to configure logging
logging.basicConfig(level=logging.DEBUG)

# return client with slug name.
def look_up_client(db, slug_name):
    return db.query(models.Client).filter(models.Client.slug == slug_name).first()

def test_ping(client_instance):
    # check root URL
    root_response = client_instance.get("/")
    assert root_response.status_code == 200
    assert root_response.json()['detail'] == "Notification Application is up"

def test_create_client(client_instance, get_session):
    # data to populate the table with.
    client_data = {
        'slug': 'client-f',
        'client_key': str(uuid.uuid4())
    }
    
    #get the client router
    client_response = client_instance.post("/client/create", json=client_data)
    
    assert client_response.status_code == 201
    assert client_response.json()['detail'] == "Client was successfully created"
    assert client_response.json()['status'] == 1
    #check the length of the table to be sure it has increased.
    retrieve_clients = models.Client.retrieve_all_client(get_session)
    assert len(retrieve_clients) == 1
    
    # check if the vaues of attributes created.
    get_details = models.Client.check_single_key(get_session, client_data['client_key'])
    assert get_details.slug == client_data['slug']
    assert get_details.client_key == client_data['client_key']
    assert get_details.status == True
    
#This function checks for error which occurs while creating the client  
def test_create_client_exist_error(client_instance, get_session):
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
    

def test_create_client_insert_error(client_instance, get_session):
    # data to populate the table with.
    client_data = {
        'slug': None,
        'client_key': str(uuid.uuid4())
    }
    
    # unprocessiable entity error.
    client_response = client_instance.post("/client/create", json=client_data)
    
    assert client_response.status_code != 201
    

def test_deactivate_client_with_middleware(client_instance, get_session):
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
    # force commit after updating.
    get_session.commit()
    assert client_response.status_code == 200
    assert client_response.json()['status'] == 1
    
    # check if it was successfully updated.
    updated_data = look_up_client(get_session, client.slug)
    assert updated_data is not None
    assert updated_data.slug == client.slug
    assert updated_data.status == False
    

def test_deactivate_client_without_middleware(client_instance, get_session):
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
    assert client_response.json()['detail'] == "Client key is missing"
 
def test_deactivate_client_with_deactivated_user(client_instance, get_session):
    # data to populate the table with.
    client_data = {
        'slug': 'client-A',
        'client_key': str(uuid.uuid4())
    }
    
    client = ClientSchema(**client_data)
    created_client = models.Client(slug=client.slug, client_key=client.client_key, status=False)
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
    # update the client status with headers
    client_response = client_instance.patch("/client/deactivate", headers=headers)
    
    assert client_response.status_code == 401
    assert client_response.json()['detail'] == "Inactive account"
 
                    
def test_update_client_key_with_middleware(client_instance, get_session):
    # data to populate the table with.
    client_data = {
        'slug': 'client-A',
        'client_key': "old client key"
    }
    # synchronizing with the schemas.
    client = ClientSchema(**client_data)
    created_client = models.Client(slug=client.slug, client_key=client.client_key)
    get_session.add(created_client)
    get_session.commit()
    
    retrieve_clients = models.Client.retrieve_all_client(get_session)
    assert len(retrieve_clients) == 1
    
    # header.
    headers = {
        "Client-Authorization": client.client_key
    }
    # update the key. 
    new_key = {
        'client_key':"new key"
    }
    
    new_key_data = UpdateClientKeySchema(**new_key)
    client_response = client_instance.patch("/client/update", json=new_key, headers=headers)
    # force commit to ensure update happens immediately.
    get_session.commit()
    assert client_response.status_code == 200
    # check if the key has been updated
    updated_data = look_up_client(get_session, client.slug)
    assert updated_data is not None
    # check if it doesn't have the key stored as old key anymore.
    # client.client_key = "Old key"
    assert updated_data.client_key != client.client_key
    # check if it was updated correctly.
    assert updated_data.slug == client.slug
    assert updated_data.status == True
    assert updated_data.client_key == "new key"
    
def test_update_client_key_with_deactivated_user(client_instance, get_session):
    # data to populate the table with.
    client_data = {
        'slug': 'client-A',
        'client_key': str(uuid.uuid4())
    }
    
    client = ClientSchema(**client_data)
    created_client = models.Client(slug=client.slug, client_key=client.client_key, status=False)
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
    # update the key. 
    new_key = {
        'client_key':"new key"
    }
    # update the client status with headers
    client_response = client_instance.patch("/client/update", json=new_key, headers=headers)
    
    assert client_response.status_code == 401
    assert client_response.json()['detail'] == "Inactive account"
    
def test_update_client_key_without_middleware(client_instance, get_session):
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
    
    # update the key. 
    new_key = {
        'client_key':"new key"
    }
    # update the client status with headers
    client_response = client_instance.patch("/client/update", json=new_key)
    
    assert client_response.status_code == 401
    assert client_response.json()['detail'] == "Client key is missing"


def test_update_client_key_with_same_key(client_instance, get_session):
    # data to populate the table with.
    client_data = {
        'slug': 'client-A',
        'client_key': "old key"
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
    # update the key. 
    new_key = {
        'client_key':"old key"
    }
    # update the client status with headers
    client_response = client_instance.patch("/client/update", json=new_key, headers=headers)
    
    assert client_response.status_code == 400
    assert client_response.json()['detail'] == "Client with such key already exists"

def test_reactivate_client(client_instance, get_session):
    # data to populate the table with.
    client_data = {
        'slug': 'client-A',
        'client_key': str(uuid.uuid4())
    }
    
    client = ClientSchema(**client_data)
    created_client = models.Client(slug=client.slug, client_key=client.client_key, status = False)
    get_session.add(created_client)
    get_session.commit()
    
    assert created_client is not None
    # check if the client is False.
    assert created_client.status == False
    # ensure it was created.
    client_response = client_instance.patch(f"/client/reactivate/1")
    get_session.commit()
    assert client_response.status_code == 200
    assert client_response.json()['status'] == 1
    # check if the key has been updated
    updated_data = look_up_client(get_session, client.slug)
    assert updated_data is not None
    assert updated_data.status == True
    
    
def test_reactivate_client_error(client_instance, get_session):
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
    
def test_get_all_clients(client_instance, get_session):
    
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
    assert client_response.status_code == 200
    
def test_get_all_clients_with_error(client_instance, get_session):
    # happens when we are accessing a page less than 0.
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
    client_response = client_instance.get("/client/", params={"page":0, "page_size":1, "page_number": 0})
    assert client_response.status_code == 422

    
    
    
    
    

    
    
    
 
    