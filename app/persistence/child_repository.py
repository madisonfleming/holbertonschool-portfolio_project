#!/usr/bin/python3

from app.persistence.repository import Repository


class ChildRepository(Repository):
    def __init__(self):
        self._storage = {}

    def add(self, child):
        self._storage[child.id] = child

    def get(self, child_id):
        return self._storage.get(child_id)

    def get_by_ids(self, child_ids: list[str]):
        return [
            child for child in self._storage.values()
            if child.id == child_ids
        ]

    def get_all(self):
        return []

    def get_by_attribute(self, attr, value):
        return None

    def update(self, id, data):
        pass

    def delete(self, id):
        pass
