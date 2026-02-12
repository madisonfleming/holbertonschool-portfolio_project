#!/usr/bin/python3

from app.persistence.repository import Repository


class ReadingSessionRepository(Repository):
    def __init__(self):
        self._storage = {}

    def add(self, session):
        self._storage[session.id] = session

    def get(self, session_id):
        return self._storage.get(session_id)

    def get_by_child(self, child_id):
        return [
            session for session in self._storage.values()
            if session.child_id == child_id
        ]

    def get_all(self):
        return []

    def get_by_attribute(self, attr, value):
        return None

    def update(self, id, data):
        pass

    def delete(self, id):
        pass
