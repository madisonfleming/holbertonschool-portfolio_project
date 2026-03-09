#!/usr/bin/python3

from app.persistence.repository import Repository
from app.domain.child import Child
from app.persistence.in_memory_seed import Childdata

class ChildRepository(Repository):
    def __init__(self):
        self._storage = Childdata().children

    def save(self, child: Child):
        self._storage[child.id] = child.to_dict()

    def get(self, child_id: str):
        data = self._storage.get(child_id)
        return Child.from_dict(data)

    def get_all(self):
        # Not needed on child_repository
        # - will be implemented on relationship_repository
        pass

    def get_by_attribute(self, attr, value):
        return None

    def update(self, id, data):
        pass

    def delete(self, id):
        pass

    def get_by_ids(self, child_ids):
        # child_ids: a list of child ids
        # returns: a list of child objects
        result = []
        for child_id in child_ids:
            child = self.get(child_id)
            if child:
                result.append(child)
        return result

