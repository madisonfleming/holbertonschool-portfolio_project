#!/usr/bin/python3

from dataclasses import asdict
from app.domain.repositories.milestone_completion_repository import MilestoneCompletionRepositoryBase
from app.domain.milestone_completion import MilestoneCompletion

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
    def __init__(self, milestone_repository): # for milestone_repository's get method below
        self._storage = MILESTONE_COMPLETIONS
        self.milestone_repository = milestone_repository # for milestone_repository's get method below

    def save(self, milestone) -> str:
        self._storage[milestone.id] = asdict(milestone)
        return milestone

    def get(self, milestone_id) -> MilestoneCompletion | None:
        data = self._storage.get(milestone_id)
        return MilestoneCompletion.from_dict(data) if data else None

    def get_all_milestones_by_child(self, child_id) -> list[MilestoneCompletion]:
        return [
            MilestoneCompletion.from_dict(c)
            for c in self._storage.values()
            if c["child_id"] == child_id
        ]

    def get_all_by_child_and_key(
        self,
        child_id,
        milestone_key
    ) -> list[MilestoneCompletion]:
        return [
            MilestoneCompletion.from_dict(m)
            for m in self._storage.values()
            if m["child_id"] == child_id
            and self.milestone_repository.get(m["milestone_id"]).type == milestone_key
        ]

    def get_most_recent_reading_milestone(
        self,
        child_id: str,
        type: str
    ) -> MilestoneCompletion | None:
        """ Used by create_reading_session to find a child's most recent milestone"""
        most_recent = max(
            (
                m for m in self._storage.values()
                if m["child_id"] == child_id
                and self.milestone_repository.get(m["milestone_id"]).type == type
            ),
            key=lambda m: datetime.fromisoformat(m["created_at"]),
            default=None
        )

        if most_recent:
            return MilestoneCompletion.from_dict(most_recent)
        return None
