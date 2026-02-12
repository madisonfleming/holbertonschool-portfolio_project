#!/usr/bin/python3

from app.persistence.repository import Repository


class MilestoneCompletionRepository(Repository):
    def __init__(self):
        self._storage = {}

    def add(self, completion):
        self._storage[completion.id] = completion

    def get(self, completion_id):
        return self._storage.get(completion_id)

    def get_by_child(self, child_id):
        return [
            c for c in self._storage.values()
            if c.child_id == child_id
        ]

    def get_all(self):
        return []

    def get_by_attribute(self, attr, value):
        return None

    def update(self, id, data):
        pass

    def delete(self, id):
        pass

    def get_by_child_and_milestone(self, child_id, milestone_id):
        for c in self._storage.values():
            if c.child_id == child_id and c.milestone_id == milestone_id:
                return c
        return None
