import db
import uvicorn
import logging
from fastapi import FastAPI
from routers import users


app = FastAPI()

# Create the users table if it does not exist
db.create_tables()

# Setup /user and /users routes
app.include_router(users.router, prefix="/users", tags=["users"])

# Setup basic logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
