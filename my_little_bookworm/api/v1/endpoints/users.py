from fastapi import APIRouter, HTTPException
from my_little_bookworm.api.v1.schemas.users import CreateUser, UserResponse, DashboardResponse
from my_little_bookworm.services.facade import MLBFacade
from my_little_bookworm.persistence.user_repository import UserRepository


router = APIRouter()
repo = UserRepository()
service = MLBFacade(repo)


@router.get("/users")
def get_users():
    # Sanity check that the GET endpoint works
    return {'Hello users!'}

@router.post("/users", response_model=UserResponse)
def create_user(req: CreateUser):
    return service.create_user(req)
    # return UserResponse(id=user.id, name=user.name, email=user.email, role=user.role)

@router.get("/users/{user_id}/dashboard", response_model=DashboardResponse)
def get_dashboard(user_id: str):
    return service.get_dashboard(user_id)
