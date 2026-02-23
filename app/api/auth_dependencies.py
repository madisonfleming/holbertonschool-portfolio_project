# All protected endpoints will call this function to verify and decode the JWT token provided by Firebase
# The function returns the decoded token to the calling endpoint OR raises an exception upon failure

from firebase_admin import auth
from firebase_admin.exceptions import FirebaseError
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.api.dependencies import MLBFacade, get_facade
from typing import TypedDict
import os   # operating system, use for testing mode

security = HTTPBearer(auto_error=False) # extract Authorization header from http request
router = APIRouter()

class CurrentUser(TypedDict):
    firebase_uid: str
    user_id: str

def authorize_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), facade: MLBFacade = Depends(get_facade)) -> CurrentUser:
    # credentials becomes a fastapi dependency object that stores scheme(Bearer) and credentials(token) at runtime

    # Toggles a test user uid to bypass protections while testing
    # Activated by running "TEST_MODE=true uvicorn app.main:app --reload"
    if os.getenv("TEST_MODE") == "true":
        return {"uid": "test-user", "user_id": "uuid1234"}
    
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    
    id_token = credentials.credentials

    try:
        decoded_token = auth.verify_id_token(id_token)
    except FirebaseError: # <- catch errors raised by firebase admin SDK (invalid/expired/revoked token etc)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Error verifying token",
        )
    
    firebase_uid = decoded_token["uid"]

    # check if custom claim already exists
    user_id = decoded_token.get("user_id")

    # if not user_id:
    #     raise HTTPException(
    #         status_code=401,
    #         detail="User claims not synced. Please refresh token."
    #     )

    # return {
    #     "uid": decoded_token["uid"],
    #     "user_id": user_id,
    # }

    if user_id:
        return user_id
    
    if not user_id:
        user = facade.get_user_from_firebase_uid(firebase_uid)
        user_id = user.id
        facade.sync_user_claim(firebase_uid)


    if not user_id:
        raise HTTPException(status_code=403, detail="User not found")
    
    return {
            "uid": decoded_token["uid"],
            "user_id": user_id,
        }


#the endpoint to use to fetch in the front end 
@router.get("/protected")
def protected_route(user_data: dict = Depends(authorize_current_user)):
    print("User data from endpoint", user_data)
    return {
        "message": "Valid Token"
    }