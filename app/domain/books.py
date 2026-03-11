from dataclasses import dataclass
from datetime import datetime

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
    created_at: datetime
    updated_at: datetime

    def to_dict(self):
        return {
            "id": self.id,
            "external_id": self.external_id,
            "source": self.source,
            "title": self.title,
            "author": self.author,
            "cover_url": self.cover_url,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            external_id=data["external_id"],
            source=data["source"],
            title=data["title"],
            author=data["author"],
            cover_url=data["cover_url"],
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
        )
