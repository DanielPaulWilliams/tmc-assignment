import logging
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from models import UsersModel
from schemas import UserSchema
from db import Session

router = APIRouter()


@router.post("/create")
def create_user(user: UserSchema):

    logging.info("Starting: create_user()")

    session = Session()

    try:

        db_user = UsersModel(
            firstname=user.firstname,
            lastname=user.lastname,
            age=user.age,
            date_of_birth=user.date_of_birth
        )
        session.add(db_user)
        session.commit()
        new_user_id = db_user.id

    except Exception as e:
        session.rollback()
        error_message = 'An error occurred when attempting to create a User.'
        logging.error({
            'error_message': error_message,
            'stack_trace': e
        })
        return JSONResponse(status_code=500, content={
            'error': error_message
        })

    finally:
        session.close()

    message = f'User with id of {new_user_id} created successfully.'
    logging.info(message)
    response = JSONResponse(
        status_code=201,
        content={
            'message': message
        }
    )

    logging.info("Completed: create_user()")

    return response


@router.get("")
def get_all_users():

    logging.info("Starting: get_all_users()")

    session = Session()

    try:

        users = session.query(UsersModel).all()
        users_list = [user.to_dict() for user in users]
        logging.debug({
            'users_list': users_list
        })

    except Exception as e:
        session.rollback()
        error_message = 'An error occurred when attempting to get the users.'
        logging.error({
            'error_message': error_message,
            'stack_trace': e
        })
        return JSONResponse(status_code=500, content={
            'error': error_message
        })

    finally:
        session.close()

    response = JSONResponse(
        status_code=200,
        content=jsonable_encoder(users_list)
    )

    logging.info("Completed: get_all_users()")

    return response


@router.delete("/{user_id}")
def delete_user(user_id: int):

    logging.info("Starting: delete_user()")

    session = Session()

    try:

        user = session.query(UsersModel).filter(UsersModel.id == user_id).first()
        if not user:
            logging.error(f"User with id {user_id} not found when attempting to delete user.")
            return JSONResponse(
                status_code=404,
                content={'error': f'User with id {user_id} not found.'},
            )
        session.delete(user)
        session.commit()

    except Exception as e:
        session.rollback()
        error_message = f'An error occurred when attempting to delete a User with id the of {user_id}.'
        logging.error({
            'error_message': error_message,
            'stack_trace': e
        })
        return JSONResponse(status_code=500, content={
            'error': error_message,
        })

    finally:
        session.close()

    message = f'User with id of {user_id} has been deleted successfully.'
    logging.info(message)

    response = JSONResponse(
        status_code=200,
        content={
            'message': message
        }
    )

    logging.info("Completed: delete_user()")

    return response
