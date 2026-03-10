from abc import ABC, abstractmethod
from app.domain.milestone_type import MilestoneType


class MilestoneTypeRepositoryBase(ABC):
    # abstract interface for accessing predefined milestone types

    @abstractmethod
    def get(self, milestone_type_id: str) -> MilestoneType:
        ...

    @abstractmethod
    def get_all_by_type(self, milestone_type: str) -> list[MilestoneType]:
        ...

    @abstractmethod
    def get_by_threshold(self, threshold: int) -> MilestoneType | None:
        ...

    @abstractmethod
    def get_by_subject(self, subject: str) -> MilestoneType | None:
        ...

    @abstractmethod
    def get_by_type_and_threshold(
        self,
        milestone_type: str,
        threshold: int
    ) -> MilestoneType | None:
        ...
