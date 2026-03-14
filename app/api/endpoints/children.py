from fastapi import APIRouter, Depends
from app.services.facade import MLBFacade
from app.api.dependencies import get_facade
from app.api.auth_dependencies import auth_current_user
from app.api.schemas.children import CreateChild, ChildResponse, UpdateChild
from typing import List

# TODO: if fb uid not needed to pass to facade - can protect all endpoints at the router level
router = APIRouter() # auth applied at individual endpoint level. 

# Requirement: Create Child
@router.post("/children", response_model=ChildResponse, status_code=201)
def create_child(
    child_data: CreateChild,
    facade: MLBFacade = Depends(get_facade),
    decoded_token: dict = Depends(auth_current_user)
    ):
    firebase_uid = decoded_token['uid']
    return facade.create_child(child_data, firebase_uid)

# Requirement: Retrieve all children
@router.get("/children", response_model=List[ChildResponse], status_code=200)
def get_children(
    facade: MLBFacade = Depends(get_facade),
    decoded_token: dict = Depends(auth_current_user)
    ):
    firebase_uid = decoded_token['uid']
    return facade.get_children(firebase_uid)

# Requirement: Retrieve a single child
@router.get("/children/{child_id}", response_model=ChildResponse, status_code=200)
def get_child(
    child_id: str,
    facade: MLBFacade = Depends(get_facade),
    decoded_token: dict = Depends(auth_current_user)
    ):
    firebase_uid = decoded_token['uid']
    return facade.get_child(child_id, firebase_uid)

# Requirement: Update a child
@router.put("/children/{child_id}", response_model=ChildResponse, status_code=200)
def update_child(
    child_id: str,
    updated_child_data: UpdateChild,
    facade: MLBFacade = Depends(get_facade),
    decoded_token: dict = Depends(auth_current_user)
    ):
    firebase_uid = decoded_token['uid']
    return facade.update_child(child_id, updated_child_data, firebase_uid) #TODO: check method name and params match facade
