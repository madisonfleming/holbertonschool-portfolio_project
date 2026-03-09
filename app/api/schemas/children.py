from pydantic import BaseModel
from datetime import date

class CreateChild(BaseModel):
    name: str
    date_of_birth: date
    avatar_url: str | None = None
    relationship_type: str | None = None

class ChildResponse(BaseModel):
    id: str
    name: str
    age: int
    avatar_url: str | None = None
    relationship_type: str
    role: str

    @classmethod
    def from_domain(cls, child, relationship_type, role):    # cls is ChildResponse
        return cls(
            id=child.id,
            name=child.name,
            age=child.age,
            avatar_url=child.avatar_url,
            relationship_type=relationship_type,
            role=role
        )


class UpdateChild(BaseModel):
    name: str | None = None
    date_of_birth: date | None = None
    avatar_url: str | None = None