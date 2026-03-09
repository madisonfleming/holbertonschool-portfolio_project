from pydantic import BaseModel
from datetime import date

from app.domain.books import Book

class BookSearchResponse(BaseModel):
    book_id: str | None = None      # optional None if external lib only
    external_id: str
    source: str         # openLibrary 
    title: str
    author: str | None = None
    cover_url: str | None = None

class BookResponse(BaseModel):
    book_id: str
    external_id: str
    source: str
    title: str
    author: str
    cover_url: str | None = None

    @classmethod
    def from_domain(cls, book: Book):
        return cls(
            book_id=book.id,
            external_id=book.external_id,
            source=book.source,
            title=book.title,
            author=book.author,
            cover_url=book.cover_url,
        )
