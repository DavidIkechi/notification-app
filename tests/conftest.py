import pytest
from fastapi import FastAPI
import sys
from sqlalchemy.orm import sessionmaker
sys.path.append("..")
from db.session import engine, Base, get_db
from db.session import Session as sess
from main import notification_app 
from fastapi.testclient import TestClient



# the scope = 'session' is called once when the test is runned accross all files.
# The code is executed for all files
@pytest.fixture(scope='session')
def db():
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    
# This is called for each test function in the test files.     
@pytest.fixture(scope='function')
def get_session(db):
    connection = engine.connect()
    transaction = connection.begin()
    session = sess(bind=connection)
    # drop and re-create all tables
    Base.metadata.drop_all(bind=connection)
    Base.metadata.create_all(bind=connection)

    try:
        yield session
        session.commit()
    finally:
        session.close()
        transaction.rollback()
        connection.close()
        
@pytest.fixture(scope="function")
def client_instance(db):    
    with TestClient(notification_app) as client_instance:
        yield client_instance
        
         
