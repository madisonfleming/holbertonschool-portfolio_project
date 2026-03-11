from dataclasses import dataclass
from datetime import datetime

"""
internal domain representation of a reading session, kept separate
from API schemas so the repository works with simple data objects
as opposed the pydantic models

to elaborate slightly, the reading session dataclass will only be used by the
repo and the facade, not the API layer, so we don't need to define
behaviour as we would with the domain models. We do need the
internal domain representation, however

I think with this section, if we wanted to expand its behaviour to track
metrics, like reading session streaks, we might need to introduce a proper
domain model. For MVP this will serve its purpose though

"""
@dataclass
class ReadingSession:
    id: str
    child_id: str
    external_id: str
    book_id: str
    title: str
    author: str
    cover_url: str
    logged_at: datetime
    created_at: datetime
    updated_at: datetime

    def to_dict(self):
        return {
            "id": self.id,
            "child_id": self.child_id,
            "external_id": self.external_id,
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "cover_url": self.cover_url,
            "logged_at": self.logged_at.isoformat(),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            child_id=data["child_id"],
            external_id=data["external_id"],
            book_id=data["book_id"],
            title=data["title"],
            author=data["author"],
            cover_url=data["cover_url"],
            logged_at=datetime.fromisoformat(data["logged_at"]),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
        )

