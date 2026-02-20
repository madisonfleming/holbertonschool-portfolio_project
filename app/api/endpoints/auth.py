from fastapi import APIRouter, Depends
from app.api.schemas.auth import AuthoriseUser, AuthoriseUserResponse
from app.services.facade import MLBFacade
from app.api.dependencies import get_facade


router = APIRouter()


@router.get("/current_user", response_model=AuthoriseUserResponse, status_code=201) #<- note: not protected as used for testing purposes
def get_user_id_from_db(
    firebase_user: AuthoriseUser,
    facade: MLBFacade = Depends(get_facade),
    ):
    return facade.get_user_id(firebase_user)