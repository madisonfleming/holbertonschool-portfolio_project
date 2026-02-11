# All protected endpoints will call this function to verify and decode the JWT token provided by Firebase
# The function returns the decoded token to the calling endpoint OR raises an exception upon failure

from firebase_admin import auth
from firebase_admin.exceptions import FirebaseError
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer() # extract Authorization header from http request
router = APIRouter() 

def auth_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    # credentials becomes a fastapi dependency object that stores scheme(Bearer) and credentials(token) at runtime 
    try:
        encoded_token = credentials.credentials # <-the token string is in credentials.credentials
        decoded_token = auth.verify_id_token(encoded_token) # verify and decode the JWT token by calling the firebase admin SDK
        return decoded_token
    except FirebaseError: # <- catch errors raised by firebase admin SDK (invalid/expired/revoked token etc)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Error verifying token",
        )
#the endpoint to use to fetch in the front end 
@router.get("/protected")
def protected_route(user_data: dict = Depends(auth_current_user)):
    return {
        "message": "Valid Token"
    }
