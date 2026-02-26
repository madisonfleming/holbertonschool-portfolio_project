from fastapi import APIRouter, Depends
from app.api.schemas.users import CreateUser, UserResponse, UpdateUser
from app.services.facade import MLBFacade
from app.api.dependencies import get_facade
from app.api.auth_dependencies import auth_current_user
from app.config import get_settings_class
from fastapi import HTTPException

router = APIRouter()

# # Requirement: Create User
# # NOTE: ENDPOINT RESTRICTED TO DEVS ONLY. THIS ENDPOINT SAVES TO REPO BY USER ID NOT FB UID - NOT TO BE USED IN PRODUCTION
# Settings = get_settings_class() # get config class in use
# settings = Settings() # create instance of class to check if app in dev mode
# @router.post("/users", response_model=UserResponse, status_code=201)
# def create_user(
#     user_data: CreateUser,
#     facade: MLBFacade = Depends(get_facade)
#     ):
#     if settings.DEBUG:
#         return facade.create_user(user_data)
#     raise HTTPException(status_code=403)

# Requirement: Retrieve a User
@router.get("/users/me", response_model=UserResponse, status_code=200)
def get_user(
    facade: MLBFacade = Depends(get_facade),
    decoded_token: dict = Depends(auth_current_user)
    ):
    firebase_uid = decoded_token["uid"]
    return facade.get_user(firebase_uid)

# Requirement: Update a User
@router.put("/users/me", response_model=UserResponse, status_code=200)
def update_user(
    updated_data: UpdateUser,
    facade: MLBFacade = Depends(get_facade),
    decoded_token: dict = Depends(auth_current_user)
    ):
    firebase_uid = decoded_token["uid"]
    return facade.update_user(updated_data, firebase_uid)
