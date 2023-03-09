import pytest
import sys
from sqlalchemy.orm import sessionmaker
sys.path.append("..")
from db.session import Session, engine, Base

# the scope = 'session' is called once when the test is runned.
# The code is executed once.
@pytest.fixture(scope='session')
def db():
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    
# This is called for each test function in the test files.     
@pytest.fixture(scope='function')
def get_session(db):
    connection = db.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()
    try:
        yield session
        session.commit()
    finally:
        session.close()
        transaction.rollback()
        connection.close()