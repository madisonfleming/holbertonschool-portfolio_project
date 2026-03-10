#!/usr/bin/python3

from app.domain.repositories.child_repository import ChildRepositoryBase
from app.domain.child import Child
from app.persistence.in_memory_seed import Childdata

class ChildRepository(ChildRepositoryBase):
    def __init__(self):
        self._storage = Childdata().children

    def save(self, child: Child) -> None:
        self._storage[child.id] = child.to_dict()

    def get(self, child_id: str) -> Child | None:
        data = self._storage.get(child_id)
        return Child.from_dict(data)

    def get_by_ids(self, child_ids) -> list[Child]:
        # child_ids: a list of child ids
        # returns: a list of child objects
        result = []
        for child_id in child_ids:
            child = self.get(child_id)
            if child:
                result.append(child)
        return result

