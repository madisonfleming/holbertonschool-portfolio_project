from fastapi import APIRouter, Depends
from app.services.facade import MLBFacade
from app.api.dependencies import get_facade
from app.api.auth_dependencies import auth_current_user
from app.api.schemas.children import CreateChild, ChildResponse, UpdateChild

# TODO: if fb uid not needed to pass to facade - protect all endpoints at the router level
router = APIRouter() # auth applied at individual endpoint level. 

# Requirement: Create Child
@router.post("/children", status_code=201) # TODO: status code returns on success, errors to be handled in new error handling logic. add response_model=ChildResponse if needed
def create_child(
    child_data: CreateChild,
    facade: MLBFacade = Depends(get_facade),
    decoded_token: dict = Depends(auth_current_user)
    ):
    firebase_uid = decoded_token['uid']
    return facade.create_child(child_data, firebase_uid) #TODO: use actual facade method name once created, check if firebase_uid is required in facade, remove if not

# Requirement: Retrieve a single child
@router.get("/children/{child_id}", response_model=ChildResponse, status_code=200)
def get_child(
    child_id: str,
    facade: MLBFacade = Depends(get_facade),
    decoded_token: dict = Depends(auth_current_user)
    ):
    firebase_uid = decoded_token['uid']
    return facade.get_child(child_id, firebase_uid) #TODO: check mathod name and params match facade




# placeholder for the momo
# FastAPI injects the shared facade instance created in app.py via Depends(get_facade)
# endpoints/reading_sessions.py has a mental model check FYI

