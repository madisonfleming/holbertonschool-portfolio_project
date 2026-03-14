#!/usr/bin/python3

from dataclasses import asdict
from app.domain.repositories.milestone_completion_repository import MilestoneCompletionRepositoryBase

"""
Note: update and delete not implemented
"""

MILESTONE_COMPLETIONS = {
    "1": {
        "id": "1",
        "child_id": "e686c824-25e6-4704-87a6-651938429111",
        "milestone_id": "1",
        "description": "Susie read 25 books out of 1000!",
        "completed_at": "2025-11-27",
        "created_at": "2025-12-02",
        "updated_at": "2025-12-02",
        "reward_generated_at": None,
        "reward_url": None,
    },
    "2": {
        "id": "2",
        "child_id": "e686c824-25e6-4704-87a6-651938429111",
        "milestone_id": "2",
        "description": "Susie read 50 books out of 1000!",
        "completed_at": "2025-12-01",
        "created_at": "2025-12-25",
        "updated_at": "2025-12-25",
        "reward_generated_at": None,
        "reward_url": None,
    },
    "3": {
        "id": "3",
        "child_id": "e686c824-25e6-4704-87a6-651938429111",
        "milestone_id": "3",
        "description": "Susie has read 5 books about elephants this week! High five!",
        "completed_at": "2025-12-01",
        "created_at": "2026-02-25",
        "updated_at": "2026-02-25",
        "reward_generated_at": None,
        "reward_url": None,
    },
    # "4": {
    #     "created_at": "2026-02-25",
    #     "updated_at": "2026-02-25",
    #     "id": "4",
    #     "name": "Read 5 Books about elephants",
    #     "description": "Billie has read 5 books about elephants this week! High five!",
    #     "type": "weekly_goals",
    #     "threshold": 5,
    #     "child_id": "e686c824-25e6-4704-87a6-651938429222",
    # }
}

# for r in MILESTONE_COMPLETIONS.values():
#     print(r)

class MilestoneCompletionRepository(MilestoneCompletionRepositoryBase):
    def __init__(self):
        self._storage = MILESTONE_COMPLETIONS

    def save(self, milestone) -> str:
        self._storage[milestone.id] = asdict(milestone)
        return milestone.id

    def get(self, milestone_id) -> dict | None:
        return self._storage.get(milestone_id)

    def get_all_milestones_by_child(self, child_id) -> list[dict]:
        for k, v in MILESTONE_COMPLETIONS.items():
            print(k, v)

    def get_all_milestones_by_child(self, child_id) -> list[dict]:
        return [
            c for c in self._storage.values()
            if c["child_id"] == child_id
        ]

    def get_all_by_child_and_key(
        self,
        child_id,
        milestone_key
    ) -> list[dict]:
        return [
            m for m in self._storage.values()
            if m["child_id"] == child_id
            and self.milestone_repository.get(m["milestone_id"]).type == milestone_key
        ]

    def get_most_recent_reading_milestone(
        self,
        child_id: str,
        type: str
    ) -> dict | None:
        """ Used by create_reading_session to find a child's most recent milestone"""
        return max(
            (
                m for m in self._storage.values()
                if m["child_id"] == child_id
                and self.milestone_repository.get(m["milestone_id"]).type == milestone_key
            ),
            key=lambda m: m["created_at"],
            default=None
        )
