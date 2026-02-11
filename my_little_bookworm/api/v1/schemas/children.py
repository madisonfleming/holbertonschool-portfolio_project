from pydantic import BaseModel

class CreateChild(BaseModel):
    name: str
    avatar_url: str | None = None

class ChildResponse(BaseModel):
    child_id: str
    name: str
    avatar_url: str | None = None

class UpdateChild(BaseModel):
    name: str | None = None
    avatar_url: str | None = None