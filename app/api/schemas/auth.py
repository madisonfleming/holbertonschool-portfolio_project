from pydantic import BaseModel


class AuthoriseUser(BaseModel):
    firebase_uid: str


class AuthoriseUserResponse(BaseModel):
    id: str
