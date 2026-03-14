from abc import ABC, abstractmethod
from datetime import datetime
from app.domain.reading_sessions import ReadingSession


class ReadingSessionRepositoryBase(ABC):
    # abstract interface for reading session persistence."""

    @abstractmethod
    def save(
        self,
        child_id: str,
        book_id: str,
        logged_at: datetime
    ) -> ReadingSession:
        ...

    @abstractmethod
    def get_by_id(self, session_id: str) -> ReadingSession | None:
        ...

    @abstractmethod
    def get_by_child(self, child_id: str) -> list[ReadingSession]:
        ...

    @abstractmethod
    def update(self, session: ReadingSession) -> ReadingSession:
        ...
