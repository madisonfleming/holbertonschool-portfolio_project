from pydantic import BaseModel
from datetime import datetime


class CreateReadingSession(BaseModel):
    child_id: str
    external_id: str
    source: str
    title: str
    author: str
    cover_url: str
    # The frontend may send this, or the backend can set it automatically
    logged_at: datetime # this is date book read per wireframe - FE checking to see if they can default this to date = today

# TODO: check attribute names against actual names returned from facade, update if required
class ReadingSessionResponse(BaseModel):
    session_id: str
    child_id: str
    book_id: str
    logged_at: datetime

    @classmethod
    def from_domain(cls, session):
        return cls(
            session_id=session.id,
            child_id=session.child_id,
            book_id=session.book_id,
            logged_at=session.logged_at
        )


class UpdateReadingSession(BaseModel):
    book_id: str | None = None
    logged_at: datetime | None = None
