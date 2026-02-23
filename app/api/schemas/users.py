from pydantic import BaseModel, EmailStr

# TODO: remove this if Create User endpoint is removed
class CreateUser(BaseModel):
    name: str
    email: EmailStr

class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: str

class UpdateUser(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
