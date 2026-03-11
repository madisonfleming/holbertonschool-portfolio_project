from abc import ABC, abstractmethod
from app.domain.milestone_completion import MilestoneCompletion


class MilestoneCompletionRepositoryBase(ABC):
    # abstract interface for milestone completion persistence

    @abstractmethod
    def save(self, milestone: MilestoneCompletion) -> str:
        ...

    @abstractmethod
    def get(self, milestone_id: str) -> MilestoneCompletion | None:
        ...

    @abstractmethod
    def get_all_milestones_by_child(self, child_id: str) -> list[MilestoneCompletion]:
        ...

    @abstractmethod
    def get_all_by_child_and_key(
        self,
        child_id: str,
        milestone_key: str
    ) -> list[MilestoneCompletion]:
        ...

    @abstractmethod
    def get_most_recent_reading_milestone(
        self,
        child_id: str,
        milestone_key: str
    ) -> MilestoneCompletion | None:
        ...
