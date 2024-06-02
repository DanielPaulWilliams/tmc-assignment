from tests.setup import test_app, client, db_session, clear_users_table
from sqlalchemy import event
from sqlalchemy.exc import SQLAlchemyError
from db import Session, engine
from models import UsersModel


# #####################################
# POST /users/create
# #####################################


# TODO - test create multiple users?
def test_create_users_success(client, db_session):
    response = client.post(
        '/users/create',
        json={
            'firstname': 'Bruce',
            'lastname': 'Wayne',
            'age': 30,
            'date_of_birth': '1939-02-19'
        },
    )
    assert response.status_code == 201
    assert response.json() == {
        "message": "User with id of 1 created successfully."
    }

    db_session.close()


def test_create_users_invalid_input(client, db_session):
    response = client.post(
        '/users/create',
        json={
            'firstname': 'Bruce',
            'age': 30,
            'date_of_birth': '1939-02-19',
        },
    )
    assert response.status_code == 422
    assert response.json() == {
        'detail': [
            {
                'type': 'missing',
                'loc': ['body', 'lastname'],
                'msg': 'Field required',
                'input': {
                    'firstname': 'Bruce',
                    'age': 30,
                    'date_of_birth': '1939-02-19'
                }
            }
        ]
    }


def test_create_users_sql_error(client, db_session):

    # Setup error to occur during commit
    def raise_commit_error(*args, **kwargs):
        raise SQLAlchemyError("Simulated database commit error")

    event.listen(Session, 'before_commit', raise_commit_error)

    response = client.post(
        '/users/create',
        json={
            'firstname': 'Bruce',
            'lastname': 'Wayne',
            'age': 30,
            'date_of_birth': '1939-02-19'
        },
    )
    assert response.status_code == 500
    assert response.json() == {
        'error': 'An error occurred when attempting to create a User.'
    }

    event.remove(Session, 'before_commit', raise_commit_error)


# #####################################
# GET /users
# #####################################

def test_get_users_success_single(client, db_session, clear_users_table):

    # Add a user to the database before making GET request
    clark_kent = UsersModel(
        firstname='Clark',
        lastname='Kent',
        age=40,
        date_of_birth='1939-02-19',
    )
    db_session.add(clark_kent)
    db_session.commit()

    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == [
        {
            'id': 2,
            'firstname': 'Clark',
            'lastname': 'Kent',
            'age': 40,
            'date_of_birth': '1939-02-19'
        }
    ]


def test_get_users_success_triple(client, db_session, clear_users_table):

    # Add 3 users to the database before making GET request
    clark_kent = UsersModel(
        firstname='Clark',
        lastname='Kent',
        age=40,
        date_of_birth='1939-02-19',
    )

    bruce_wayne = UsersModel(
        firstname='Bruce',
        lastname='Wayne',
        age=35,
        date_of_birth='1939-05-27',
    )

    princess_diana = UsersModel(
        firstname='Diana',
        lastname='Prince',
        age=30,
        date_of_birth='1941-10-21',
    )

    db_session.add_all([clark_kent, bruce_wayne, princess_diana])
    db_session.commit()

    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) == 3
    assert response.json() == [
        {'id': 3, 'firstname': 'Clark', 'lastname': 'Kent', 'age': 40, 'date_of_birth': '1939-02-19'},
        {'id': 4, 'firstname': 'Bruce', 'lastname': 'Wayne', 'age': 35, 'date_of_birth': '1939-05-27'},
        {'id': 5, 'firstname': 'Diana', 'lastname': 'Prince', 'age': 30, 'date_of_birth': '1941-10-21'}
    ]


def test_get_users_sql_error(client, db_session, clear_users_table):
    def raise_query_error(conn, cursor, statement, parameters, context, executemany):
        raise SQLAlchemyError("Simulated database query error")

    event.listen(engine, 'before_cursor_execute', raise_query_error)

    response = client.get("/users")
    assert response.status_code == 500
    assert response.json() == {
        'error': 'An error occurred when attempting to get the users.'
    }

    event.remove(engine, 'before_cursor_execute', raise_query_error)


# #####################################
# DELETE users/{user_id}
# #####################################


def test_delete_user_success(client, db_session):

    # Add user to db that will be deleted
    clark_kent = UsersModel(
        firstname='Clark',
        lastname='Kent',
        age=40,
        date_of_birth='1939-02-19',
    )
    db_session.add(clark_kent)
    db_session.commit()

    response = client.delete(
        f'/users/{clark_kent.id}'
    )
    assert response.status_code == 200
    assert response.json() == {
        'message': f'User with id of {clark_kent.id} has been deleted successfully.',
    }

    # Ensure the User has been deleted from the db
    user = db_session.query(UsersModel).filter_by(id=clark_kent.id).first()
    assert user is None


def test_delete_user_not_found(client, db_session):

    response = client.delete(
        '/users/123'
    )
    assert response.status_code == 404
    assert response.json() == {
        'error': 'User with id 123 not found.'
    }


def test_delete_user_sql_error(client, db_session):

    # Setup error to occur during commit
    def raise_commit_error(*args, **kwargs):
        raise SQLAlchemyError("Simulated database commit error")

    # Add user to db that will be deleted
    clark_kent = UsersModel(
        firstname='Clark',
        lastname='Kent',
        age=40,
        date_of_birth='1939-02-19',
    )
    db_session.add(clark_kent)
    db_session.commit()

    event.listen(Session, 'before_commit', raise_commit_error)

    response = client.delete(
        f'/users/{clark_kent.id}'
    )
    assert response.status_code == 500
    assert response.json() == {
        'error': f'An error occurred when attempting to delete a User with id the of {clark_kent.id}.'
    }

    event.remove(Session, 'before_commit', raise_commit_error)
