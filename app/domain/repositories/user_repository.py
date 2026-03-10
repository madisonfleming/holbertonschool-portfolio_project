from abc import ABC, abstractmethod
from typing import Optional
from app.domain.user import User


class UserRepositoryBase(ABC):
    # abstract interface for user persistence.

    @abstractmethod
    def save(self, user: User) -> None:
        ...

    @abstractmethod
    def get(self, user_id: str) -> User | None:
        ...

    @abstractmethod
    def get_by_firebase_uid(self, firebase_uid: str) -> User | None:
        ...

    @abstractmethod
    def get_by_email(self, email: str) -> User | None:
        ...
