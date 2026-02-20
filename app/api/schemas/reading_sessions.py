from pydantic import BaseModel
from datetime import datetime


class CreateReadingSession(BaseModel):
    child_id: str
    book_id: str
    # The frontend may send this, or the backend can set it automatically
    logged_at: datetime # this is date book read per wireframe - FE checking to see if they can default this to date = today

# TODO: check attribute names against actual names returned from facade, update if required
class ReadingSessionResponse(BaseModel):
    session_id: str
    child_id: str
    book_id: str
    logged_at: datetime

class UpdateReadingSession(BaseModel):
    child_id: str | None = None
    book_id: str | None = None
    logged_at: datetime | None = None
