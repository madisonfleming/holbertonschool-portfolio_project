from pydantic import BaseModel, EmailStr

class CreateUser(BaseModel):
    name: str
    email: EmailStr

class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: str

    @classmethod
    def from_domain(cls, user): # cls is UserResponse
        return cls(
            id=user.id,
            name=user.name,
            email=user.email,
            role=user.role
        )

class UpdateUser(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
