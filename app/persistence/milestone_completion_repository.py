#!/usr/bin/python3

from app.persistence.repository import Repository

MILESTONE_COMPLETIONS = {
    "1": {
        "created_at": "2025-12-02",
        "updated_at": "2025-12-02",
        "id": "1",
        "name": "Read 25 Books",
        "description": "Susie read 25 books out of 1000!",
        "metric_key": "books_read",
        "threshold": 25,
        "child_id": "e686c824-25e6-4704-87a6-651938429111",
    },
    "2": {
        "created_at": "2025-12-25",
        "updated_at": "2025-12-25",
        "id": "2",
        "name": "Read 50 Books",
        "description": "Susie read 50 books out of 1000!",
        "metric_key": "books_read",
        "threshold": 50,
        "child_id": "e686c824-25e6-4704-87a6-651938429111",
    },
    "3": {
        "created_at": "2026-02-25",
        "updated_at": "2026-02-25",
        "id": "3",
        "name": "Read 5 Books about elephants",
        "description": "Susie has read 5 books about elephants this week! High five!",
        "metric_key": "weekly_goals",
        "threshold": 5,
        "child_id": "e686c824-25e6-4704-87a6-651938429111",
    },
    "4": {
        "created_at": "2026-02-25",
        "updated_at": "2026-02-25",
        "id": "4",
        "name": "Read 5 Books about elephants",
        "description": "Billie has read 5 books about elephants this week! High five!",
        "metric_key": "weekly_goals",
        "threshold": 5,
        "child_id": "e686c824-25e6-4704-87a6-651938429222",
    }
}

# for r in MILESTONE_COMPLETIONS.values():
#     print(r)

class MilestoneCompletionRepository(Repository):
    def __init__(self):
        self._storage = MILESTONE_COMPLETIONS

    def save(self, milestone):
        self._storage[milestone.id] = milestone.to_dict()
        return milestone.id

    def get(self, milestone_id):
        return self._storage.get(milestone_id)

    def get_all_milestones_by_child(self, child_id):
        return [
            c for c in self._storage.values()
            if c["child_id"] == child_id
        ]

    def get_all(self):
        return []

    def get_by_attribute(self, attr, value):
        return None

    def update(self, id, data):
        pass

    def delete(self, id):
        pass

    def get_all_by_child_and_key(self, child_id, milestone_key):
        return ((m for m in self._storage.values()
            if m["child_id"] == child_id
            and m["metric_key"] == milestone_key),
            None)


    def get_most_recent_reading_milestone(self, child_id: str, metric_key: str):
        """ Used by create_reading_session to find a child's most recent milestone"""
        return max(
            (
                m for m in self._storage.values()
                if m["child_id"] == child_id
                and m["metric_key"] == metric_key
            ),
            key=lambda m: m["created_at"],
            default=None
        )