from fastapi import APIRouter, Depends
from app.services.facade import MLBFacade
from app.api.dependencies import get_facade
from app.api.auth_dependencies import authorize_current_user
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth

security = HTTPBearer(auto_error=False) # extract Authorization header from http request
router = APIRouter()

@router.post("/auth/sync")
def sync_claim(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    facade: MLBFacade = Depends(get_facade),
):
    decoded = auth.verify_id_token(credentials.credentials)
    facade.sync_user_claim(decoded["uid"])
    return {"message": "Claims synced. Refresh token."}