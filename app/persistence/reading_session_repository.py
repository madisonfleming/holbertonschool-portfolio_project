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

    def save(self, session: ReadingSession) -> ReadingSession:
        
        now = datetime.now()

        if session.id is None:
            session.id = str(uuid4())
            session.created_at = now
        
        session.updated_at = now

        self._storage[session.id] = session.to_dict()
        return session

    def get_by_id(self, id: str) -> ReadingSession | None:
        data = self._storage.get(id)
        if not data:
            return None
        return ReadingSession.from_dict(data)

    def get_by_child(self, child_id: str) -> list[ReadingSession]:
        return [
            ReadingSession.from_dict(session)
            for session in self._storage.values()
            if session["child_id"] == child_id
        ]

    def update(self, session: ReadingSession) -> ReadingSession:
        session.updated_at = datetime.now()
        self._storage[session.id] = session.to_dict()
        return session
