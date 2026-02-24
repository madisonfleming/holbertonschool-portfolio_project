from pydantic import BaseModel, EmailStr

class RegisterUser(BaseModel):
    firebase_uid: str
    name: str
    email: EmailStr


class CreateUser(BaseModel):
    name: str
    email: EmailStr


class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: str
