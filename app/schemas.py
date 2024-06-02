from pydantic import BaseModel, Field
from datetime import date, datetime


# Declare the User Schema. This is the schema that is used for API serialisation and deserialisation.
class UserSchema(BaseModel):
    firstname: str
    lastname: str
    age: int = Field(default=None)
    date_of_birth: date
