## Users Application

### Introduction

This application exposes the three following endpoints:
- Create a user: `POST /users/create`
- Get all users: `GET /users`
- Delete a user: `DELETE /users/{user_id}`

This application comprises two services. A FastAPI used for the requests and Postgres for the database.

### Running

You can run this application using:

`docker-compose up`

Once this application is up and running you will then be able to make requests against it on `127.0.0.1:8000`.

You can also run the FastAPI app directly using the following steps:

1. `cd app/`
2. `uvicorn main:app --reload`

You'll also need to ensure that a local version of Postgres is running when running the app directly. See the **Testing** step below for more information.


### Testing

In order to test this application locally follow these steps:

1. Ensure you're running within a virtual environment such as venv in order to prevent package issues on your local machine. 
   1. Install virtualenv: `pip install virtualenv`
   2. Create a new virtualenv environment: `python -m venv myenv`
   3. Activate the virtualenv: `source venv/bin/activate`
2. Install all the Python package dependencies using pip.
    1. `pip install -r app/requirements.txt`
3. Set up a local Postgres database. 
   1. You do not need to create the Users table but the option is available if you wish to run the service directly (rather than through docker-compose or pytest). You can find the SQL to create the Users table in the file `create_users.sql` in the main directory.
4. In `app/db.py` modify the `DATABASE_URI` value to point to your preferred local postgres db. Ensure you've reverted this value back when running against the docker-compose instance of the postgres db.
5. Run Pytest (verbose).
    1. `pytest -v`


## API Documentation

Please see the following documentation for each API and the expected responses. 

There also exists a Postman collection, see `postman_collection.json`.

### Create a User

#### Request:

```
POST: /users/create

Body: 
{
    "firstname": "Bruce",
    "lastname": "Wayne",
    "age": 39,
    "date_of_birth": "1990-01-01"
}
```

#### Responses:

**200 Success**
```
{
    "message": "User with id of {user_id} created successfully."
}
```

**422 Unprocessable Content**

Example with lastname missing.
```
"detail": [
   {
       "type": "missing",
       "loc": ["body", "lastname"],
       "msg": "Field required",
       "input": {
           "firstname": "Bruce",
           "age": 30,
           "date_of_birth": "1939-02-19"
       }
   }
]
```

**500 Internal Server Error**
```
{
    "error": "An error occurred when attempting to create a User."
}
```



### Get all Users


```
GET: /users
```

#### Responses:

**200 Success**
```
[
   {
      "id": 1,
      "firstname": "Clark",
      "lastname": "Kent",
      "age": 40,
      "date_of_birth": "1939-02-19"
   },
   // next user in list
]
```

**500 Internal Server Error**
```
{
    "error": "An error occurred when attempting to get the users."
}
```

### Delete a User

```
DELETE: /users/{user_id}
```

#### Responses:

**200 Success**
```
{
    "message": "User with id of {user_id} has been deleted successfully."
}
```

**404 Not Found**
```
{
   "error": "User with id {user_id} not found."   
}
```

**500 Internal Server Error**
```
{
    "error": "An error occurred when attempting to delete a User with id the of {user_id}."
}
```


