#!/usr/bin/python3

from app.domain.repositories.milestone_repository import MilestoneTypeRepositoryBase
from app.domain.milestone_type import MilestoneType

"""
This table holds a pre-defined list of milestone types

Used as reference data by milestone_completion_repo

Supports:
- get (by id), useful for creating a new milestone_completion record
- get_all_by_type, useful for looking up a list of milestones defined for a given type
- get_by_subject, useful for finding a weekly goal milestone
- get_by_threshold, which might not end up being used
- get_by_type_and_threshold, useful for finding the next books_read milestone

Doesn't need:
- save
"""
# from app.persistence.repository import Repository

MILESTONE_TYPES = {
    "1": {
        "id": "1",
        "name": "Read 25 Books",
        "subject": None,
        "type": "books_read",
        "threshold": 25,
    },
    "2": {
        "id": "2",
        "name": "Read 50 Books",
        "subject": None,
        "type": "books_read",
        "threshold": 50
    },
    "3": {
        "id": "3",
        "name": "Read 5 Elephant Books",
        "subject": "elephants",
        "type": "weekly_goal",
        "threshold": 5,
    }
}

# for m in MILESTONE_TYPES.values():
#     print(m)

class MilestoneTypeRepository(MilestoneTypeRepositoryBase):
    def __init__(self):
        self._storage = MILESTONE_TYPES

    def _to_domain(self, data: dict) -> MilestoneType:
        return MilestoneType(
            id=data["id"],
            name=data["name"],
            subject=data["subject"],
            type=data["type"],
            threshold=data["threshold"],
        )

    def get(self, id: str) -> MilestoneType | None:
        data = self._storage.get(id)
        if not data:
            return None
        return self._to_domain(data)
    
    def get_all_by_type(self, milestone_type: str) -> list[MilestoneType]:
        results = []
        
        for m in self._storage.values():
            if m["type"] == milestone_type:
                results.append(self._to_domain(m))
    
    def get_by_threshold(self, threshold: int) -> MilestoneType | None:
        """ Expects that threshold values are unique in the Milestone table """
        for m in self._storage.values():
            if m["threshold"] == threshold:
                return self._to_domain(m)
        return None
    
    def get_by_subject(self, subject: str | None) -> MilestoneType | None:
        """ Possibly useful for weekly goals? """
        # print(self._storage.values())
        for m in self._storage.values():
            if m["subject"] == subject:
                return self._to_domain(m)
        return None
    
    def get_by_type_and_threshold(
        self,
        milestone_type: str,
        threshold: int,
    ) -> MilestoneType | None:
        for m in self._storage.values():
            if m["type"] == milestone_type and m["threshold"] == threshold:
                return self._to_domain(m)
        return None
