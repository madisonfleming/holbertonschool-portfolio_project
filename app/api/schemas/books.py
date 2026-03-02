from pydantic import BaseModel
from datetime import date

class BookSearchResponse(BaseModel):
    book_id: str | None = None      # optional None if external lib only
    external_id: str
    source: str         # openLibrary 
    title: str
    author: str | None = None
    cover_url: str | None = None

class BookResponse(BaseModel):
    book_id: str
    title: str
    author: str
    description: str | None = None
    cover_url: str | None = None