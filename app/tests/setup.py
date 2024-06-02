import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError
from db import Base, engine, Session
from models import UsersModel
from main import app


@pytest.fixture(scope='module')
def test_app():
    Base.metadata.create_all(engine)
    yield TestClient(app)
    Base.metadata.drop_all(engine)


@pytest.fixture(scope='module')
def client(test_app):
    return test_app


@pytest.fixture(scope='module')
def db_session():
    session = Session()
    yield session
    session.close()

@pytest.fixture(scope='function')
def clear_users_table():
    db = Session()
    try:
        db.query(UsersModel).delete()
        db.commit()
    except SQLAlchemyError:
        db.rollback()
    finally:
        db.close()
