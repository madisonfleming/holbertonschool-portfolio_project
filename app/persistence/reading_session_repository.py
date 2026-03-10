#!/usr/bin/python3

from app.domain.reading_sessions import ReadingSession
from app.domain.repositories.reading_session_repository import ReadingSessionRepositoryBase

from datetime import datetime
from uuid import uuid4

"""
Note: no delete method implemented
"""

class ReadingSessionRepository(ReadingSessionRepositoryBase):
    def __init__(self):
        self._storage = {}

    def save(
        self,
        child_id: str,
        external_id: str,
        book_id: str,
        title: str,
        cover_url: str,
        logged_at: datetime,
    ) -> ReadingSession:
        session = ReadingSession(
            id=str(uuid4()),
            child_id=child_id,
            external_id=external_id,
            book_id=book_id,
            title=title,
            cover_url=cover_url,
            logged_at=logged_at,
        )
        self._storage[session.id] = session
        return session

    def get_by_id(self, id: str) -> ReadingSession | None:
        return self._storage.get(id)

    def get_by_child(self, child_id: str) -> list[ReadingSession]:
        return [
            session for session in self._storage.values()
            if session.child_id == child_id
        ]

    def update(self, session: ReadingSession) -> ReadingSession:
        self._storage[session.id] = session
        return session
