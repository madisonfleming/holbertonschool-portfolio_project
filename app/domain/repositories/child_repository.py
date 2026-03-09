from abc import ABC, abstractmethod
from app.domain.child import Child


class ChildRepositoryBase(ABC):
    # abstract interface for child persistence

    @abstractmethod
    def save(self, child: Child) -> None:
        ...

    @abstractmethod
    def get(self, child_id: str) -> Child | None:
        ...

    @abstractmethod
    def get_by_ids(self, child_ids: list[str]) -> list[Child]:
        ...
