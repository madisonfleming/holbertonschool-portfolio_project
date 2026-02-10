from pydantic import BaseModel
from datetime import datetime


class CreateReadingSession(BaseModel):
    child_id: str
    book_id: str
    # The frontend may send this, or the backend can set it automatically
    logged_at: datetime


class ReadingSessionResponse(BaseModel):
    session_id: str
    child_id: str
    book_id: str
    logged_at: datetime
