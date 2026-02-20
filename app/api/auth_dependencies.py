# All protected endpoints will call this function to verify and decode the JWT token provided by Firebase
# The function returns the decoded token to the calling endpoint OR raises an exception upon failure

from firebase_admin import auth
from firebase_admin.exceptions import FirebaseError
from fastapi import Depends, HTTPException, status, APIRouter, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.api.endpoints.auth import get_user_id_from_db
import os   # operating system, use for testing mode

security = HTTPBearer(auto_error=False) # extract Authorization header from http request
router = APIRouter() 

def authorize_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    # credentials becomes a fastapi dependency object that stores scheme(Bearer) and credentials(token) at runtime

    # Toggles a test user uid to bypass protections while testing
    # Activated by running "TEST_MODE=true uvicorn app.main:app --reload"
    if os.getenv("TEST_MODE") == "true":
        return {"uid": "test-user", "user_id": "uuid1234"}
    
    if not credentials or credentials.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    
    id_token = credentials.split("Bearer ")[1]

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

    if user_id:
        return user_id
    
    internal_user_id = get_user_id_from_db(firebase_uid)

    if not internal_user_id:
        raise HTTPException(status_code=403, detail="User not found")
    
    # set custom claim
    # Important: client must refresh token after this request - ask FE to implement refresh
    auth.set_custom_user_claims(
        firebase_uid,
        {"user_id": internal_user_id}
    )

    return internal_user_id

#the endpoint to use to fetch in the front end 
@router.get("/protected")
def protected_route(user_data: dict = Depends(authorize_current_user)):
    print("User data from endpoint", user_data)
    return {
        "message": "Valid Token"
    }