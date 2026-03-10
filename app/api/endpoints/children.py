from fastapi import APIRouter, Depends
from app.services.facade import MLBFacade
from app.api.dependencies import get_facade
from app.api.auth_dependencies import auth_current_user
from app.api.schemas.children import CreateChild, ChildResponse, UpdateChild
from typing import List

router = APIRouter() # auth applied at individual endpoint level

# Requirement: Create Child
@router.post("/children", response_model=ChildResponse, status_code=201)
def create_child(
    child_data: CreateChild,
    facade: MLBFacade = Depends(get_facade),
    decoded_token: dict = Depends(auth_current_user)
    ):
    firebase_uid = decoded_token['uid']
    child, relationship_type, role = facade.create_child(child_data, firebase_uid)
    return ChildResponse.from_domain(child, relationship_type, role) 

# Requirement: Retrieve all children
@router.get("/children", response_model=List[ChildResponse], status_code=200)
def get_children(
    facade: MLBFacade = Depends(get_facade),
    decoded_token: dict = Depends(auth_current_user)
    ):
    firebase_uid = decoded_token['uid']
    children = facade.get_children(firebase_uid)
    result = []
    for child, relationship_type, role in children:
        response = ChildResponse.from_domain(child, relationship_type, role)
        result.append(response) 
    return result

# Requirement: Retrieve a single child
@router.get("/children/{child_id}", response_model=ChildResponse, status_code=200)
def get_child(
    child_id: str,
    facade: MLBFacade = Depends(get_facade),
    decoded_token: dict = Depends(auth_current_user)
    ):
    firebase_uid = decoded_token['uid']
    child, relationship_type, role = facade.get_child(child_id, firebase_uid)
    return ChildResponse.from_domain(child, relationship_type, role)

# Requirement: Update a child
@router.put("/children/{child_id}", response_model=ChildResponse, status_code=200)
def update_child(
    child_id: str,
    updated_child_data: UpdateChild,
    facade: MLBFacade = Depends(get_facade),
    decoded_token: dict = Depends(auth_current_user)
    ):
    firebase_uid = decoded_token['uid']
    child, relationship_type, role = facade.update_child(child_id, updated_child_data, firebase_uid)
    return ChildResponse.from_domain(child, relationship_type, role)
