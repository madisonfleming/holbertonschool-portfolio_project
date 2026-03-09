from abc import ABC, abstractmethod


class RelationshipRepositoryBase(ABC):
    # abstract interface for managing user–child relationship records.
    

    @abstractmethod
    def get(self, relationship_id: str) -> dict:
        ...

    @abstractmethod
    def get_relationship_type(
        self,
        user_id: str,
        child_id: str
    ) -> dict | None:
        ...

    @abstractmethod
    def create_relationship(
        self,
        user_id: str,
        child_id: str,
        role: str
    ) -> str:
        ...

    @abstractmethod
    def has_role(self, user_id: str, child_id: str, role: str) -> bool:
        ...

    @abstractmethod
    def has_one_of_roles(
        self,
        user_id: str,
        child_id: str,
        roles: List[str],
    ) -> bool:
        ...

    @abstractmethod
    def get_children_per_user(self, user_id: str) -> list[dict]:
        ...

    @abstractmethod
    def has_relationship(self, user_id: str, child_id: str) -> bool:
        ...
