class BookSearchResponse(BaseModel):
    book_id: str | None      # optional None if external lib only
    external_id: str
    source: str         # openLibrary 
    title: str
    author: str | None
    description: str | None
    cover_url: str | None

class BookResponse(BaseModel):
    book_id: str
    title: str
    author: str
    description: str | None
    cover_url: str | None