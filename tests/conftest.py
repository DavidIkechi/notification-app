import pytest
import sys
from sqlalchemy.orm import sessionmaker
sys.path.append("..")
from db.session import Session, db_engine, Base

@pytest.fixture(scope='session')
def db():
    Base.metadata.create_all(bind=db_engine)
    yield db_engine
    Base.metadata.drop_all(bind=db_engine)
    
@pytest.fixture(scope='function')
def session(db):
    connection = db.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()
    yield session
    session.close()
    transaction.rollback()
    connection.close()