from pydantic import BaseModel

class CreateChild(BaseModel):
    name: str
    avatar_url: str | None = None

class ChildResponse(BaseModel):
    id: str
    name: str
    age: int
    avatar_url: str | None = None

    @classmethod
    def from_domain(cls, child):    # cls is ChildResponse
        return cls(
            id=child.id,
            name=child.name,
            age=child.age,
            avatar_url=child.avatar_url
        )


class UpdateChild(BaseModel):
    name: str | None = None
    avatar_url: str | None = None