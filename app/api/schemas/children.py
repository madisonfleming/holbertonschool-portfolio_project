from pydantic import BaseModel
from datetime import date

class CreateChild(BaseModel):
    name: str
    date_of_birth: date
    avatar_url: str | None = None

class ChildResponse(BaseModel):
    child_id: str
    name: str
    age: int
    avatar_url: str | None = None

class UpdateChild(BaseModel):
    name: str | None = None
    date_of_birth: date | None = None
    avatar_url: str | None = None