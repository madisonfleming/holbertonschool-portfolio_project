#!/usr/bin/python3

from app.domain.reading_sessions import ReadingSession

from datetime import datetime
from uuid import uuid4


class ReadingSessionRepository:
    def __init__(self):
        self._storage = {}

    def save(
        self,
        child_id: str,
        book_id: str,
        logged_at: datetime
    ):
        session = ReadingSession(
            id=str(uuid4()),
            child_id=child_id,
            book_id=book_id,
            logged_at=logged_at
        )
        self._storage[session.id] = session
        return session

    def get_by_id(self, id: str):
        return self._storage.get(id)

    def get_by_child(self, child_id: str):
        return [
            session for session in self._storage.values()
            if session.child_id == child_id
        ]

    def get_all(self):
        return []

    def update(self, session: ReadingSession):
        self._storage[session.id] = session
        return session

    def delete(self, id):
        pass
