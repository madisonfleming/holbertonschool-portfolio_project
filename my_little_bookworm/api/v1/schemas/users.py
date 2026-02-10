from pydantic import BaseModel


class CreateUser(BaseModel):
    name: str
    email: str


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    role: str
