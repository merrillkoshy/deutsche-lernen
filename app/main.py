from fastapi import FastAPI

import app.models
from app.database import SessionLocal, engine

app.models.Base.metadata.create_all(bind=engine)

fastapp = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


import app.routes  # Add this line to import the routes module
