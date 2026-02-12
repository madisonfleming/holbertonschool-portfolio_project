from fastapi import FastAPI, Depends
from app.api.endpoints import users, children, milestones, reading_sessions 
from app.api.dependencies import get_facade
from app.config import firebase

import logging
logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

# router registrations
app.include_router(users.router, dependencies=[Depends(get_facade)])
app.include_router(children.router, dependencies=[Depends(get_facade)])
app.include_router(milestones.router, dependencies=[Depends(get_facade)])
app.include_router(reading_sessions.router, dependencies=[Depends(get_facade)])

# root health check
@app.get("/")
def root():
    return {"status": "OK"}

# @app.get("/users")
# def read_root():
#     return {"Hello": "Users"}

# @app.post("/users")
# def create_user(name: str, email: str):
#     user = facade.create_user(name, email)
#     return {'success': 'hello'}
