from dataclasses import dataclass

"""
internal domain representation of a stored book, kept separate
from API schemas so the repository works with simple data objects
as opposed the pydantic models

to elaborate slightly, the book dataclass will only be used by the
repo and the facade, not the API layer, so we don't need to define
behaviour as we would with the domain models. We do need the
internal domain representation, however
"""
@dataclass
class Book:
    id: str
    external_id: str
    source: str
    title: str
    author: str | None
    cover_url: str | None
