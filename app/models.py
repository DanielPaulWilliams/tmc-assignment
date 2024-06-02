from sqlalchemy import Column, String, Integer, Date
from db import Base


# Declare Users Model schema. This is the schema that is coupled with the postgres db.
class UsersModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    firstname = Column(String(250), nullable=False)
    lastname = Column(String(250), nullable=False)
    age = Column(Integer, nullable=False)
    date_of_birth = Column(Date, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'age': self.age,
            'date_of_birth': self.date_of_birth
        }
