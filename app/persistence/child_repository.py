#!/usr/bin/python3

from app.persistence.repository import Repository


class ChildRepository(Repository):
    def __init__(self):
        self._storage = {}

    def add(self, child):
        self._storage[child.id] = child

    def get(self, child_id):
        return self._storage.get(child_id)

    def get_by_user(self, user_id):
        return [
            child for child in self._storage.values()
            if child.user_id == user_id
        ]

    def get_all(self):
        return []

    def get_by_attribute(self, attr, value):
        return None

    def update(self, id, data):
        pass

    def delete(self, id):
        pass
