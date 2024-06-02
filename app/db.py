from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session

# For testing against local a postgres db
# DATABASE_URI = "postgresql+psycopg2://postgres:postgres@localhost/tmc-assignment"

# For docker-compose postgres db
DATABASE_URI = "postgresql+psycopg2://myuser:mypassword@db/mydatabase"


engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


# Set up db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    Base.metadata.create_all(bind=engine)
