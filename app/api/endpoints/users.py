from fastapi import APIRouter, Depends
from app.api.schemas.users import CreateUser, UserResponse, UpdateUser
from app.services.facade import MLBFacade
from app.api.dependencies import get_facade
from app.api.auth_dependencies import auth_current_user

# TODO: if fb uid/user_id not needed to pass to facade - can protect all endpoints at the router level with: router = APIRouter(dependencies=[Depends(auth_current_user)])
router = APIRouter() # note: auth applied at individual endpoint level for now. 

# Requirement: Create User
# TODO: check if we need this endpoint at all since we are seeding db with primary (and maybe secondary) user details
@router.post("/users", response_model=UserResponse, status_code=201)
def create_user(
    user_data: CreateUser,
    facade: MLBFacade = Depends(get_facade),
    decoded_token: dict = Depends(auth_current_user) # protects endpoint but logic for this endpoint needs to be confirmed and fixed
    ):
    firebase_uid = decoded_token["uid"]
    return facade.create_user(user_data, firebase_uid)

# Requirement: Retrieve a User
@router.get("/users/me", response_model=UserResponse, status_code=200)
def get_user(
    facade: MLBFacade = Depends(get_facade),
    decoded_token: dict = Depends(auth_current_user)
    ):
    firebase_uid = decoded_token["uid"]
    return facade.get_user(firebase_uid) #TODO: check method and params match facade

# Requirement: Update a User
@router.put("/users/me", response_model=UserResponse, status_code=200)
def update_user(
    updated_data: UpdateUser,
    facade: MLBFacade = Depends(get_facade),
    decoded_token: dict = Depends(auth_current_user)
    ):
    firebase_uid = decoded_token["uid"]
    return facade.update_user(updated_data, firebase_uid) #TODO: check method and params match facade


# <-- TODO: Remove below if not required -->

# @router.get("/users/{user_id}/dashboard", response_model=DashboardResponse)
# def get_dashboard(user_id: str, decoded_token: dict = Depends(auth_current_user)): #<- protected
#     fb_uid = decoded_token["uid"]
#     return facade.get_dashboard(user_id, fb_uid) 
"""
To do:
DashboardResponse schema to be entered in users.py
get_dashboard method to be entered in facade.py
uncomment above router
remove user_id as we need to return user profile based on their firebase uid in repo instead
"""
