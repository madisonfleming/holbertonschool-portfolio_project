from fastapi import APIRouter, Depends
from app.services.facade import MLBFacade
from app.api.dependencies import get_facade
from app.api.auth_dependencies import auth_current_user

router = APIRouter(dependencies=[Depends(auth_current_user)]) #<- attaches auth dependency to all routes in this file

@router.get("/reading_sessions")
def reading_sessions_placeholder(facade: MLBFacade = Depends(get_facade)):
    return {"status": "ok"}
# placeholder for the momo
# FastAPI injects the shared facade instance created in app.py via Depends(get_facade)

"""
Mental model check:

services/facade.py
    defines the MLBFacade class

app.py
    creates ONE instance of MLBFacade
    wires all repositories into it
    exposes it via get_facade()
    injects it into all routers

routers
    receive the shared facade via Depends(get_facade)
    (never create their own facade)

"""
