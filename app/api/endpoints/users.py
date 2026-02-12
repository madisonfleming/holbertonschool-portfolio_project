from fastapi import APIRouter, Depends
from app.api.schemas.users import CreateUser, UserResponse
from app.services.facade import MLBFacade
from app.api.dependencies import get_facade

router = APIRouter()


@router.get("/users")
def get_users():
    # Sanity check that the GET endpoint works
    return {'Hello users!'}

@router.post("/users", response_model=UserResponse)
def create_user(req: CreateUser, facade: MLBFacade = Depends(get_facade)):
    return facade.create_user(req)
    # return UserResponse(id=user.id, name=user.name, email=user.email, role=user.role)

# @router.get("/users/{user_id}/dashboard", response_model=DashboardResponse)
# def get_dashboard(user_id: str):
#     return service.get_dashboard(user_id)
"""
To do:
DashboardResponse schema to be entered in users.py
get_dashboard method to be entered in facade.py
uncomment above router
"""
