from abc import ABC, abstractmethod


class MilestoneCompletionRepositoryBase(ABC):
    # abstract interface for milestone completion persistence

    @abstractmethod
    def save(self, milestone: dict) -> str:
        ...

    @abstractmethod
    def get(self, milestone_id: str) -> dict | None:
        ...

    @abstractmethod
    def get_all_milestones_by_child(self, child_id: str) -> list[dict]:
        ...

    @abstractmethod
    def get_all_by_child_and_key(
        self,
        child_id: str,
        milestone_key: str
    ) -> list[dict]:
        ...

    @abstractmethod
    def get_most_recent_reading_milestone(
        self,
        child_id: str,
        milestone_key: str
    ) -> dict | None:
        ...
