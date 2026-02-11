#!/usr/bin/python3

from my_little_bookworm.persistence.repository import Repository


class MilestoneRepository(Repository):
    def __init__(self):
        self._storage = {}

    def add(self, milestone_type):
        self._storage[milestone_type.id] = milestone_type

    def get(self, ms_type_id):
        return self._storage.get(ms_type_id)

    def get_all(self):
        return list(self._storage.values())

    def get_by_attribute(self, attr, value):
        return None

    def update(self, id, data):
        pass

    def delete(self, id):
        pass
