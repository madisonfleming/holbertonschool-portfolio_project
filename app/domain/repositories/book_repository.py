from abc import ABC, abstractmethod
from app.domain.books import Book


class BookRepositoryBase(ABC):
    # abstract interface for book persistence

    @abstractmethod
    def search(
        self,
        query: str,
        subjects: list[str] | None = None,
        limit: int | None = None
    ) -> Book | None:
        ...

    @abstractmethod
    def get(self, book_id: str) -> Book | None:
        ...

    @abstractmethod
    def get_by_external_id(
        self,
        external_id: str,
        source: str
    ) -> Book | None:
        ...

    @abstractmethod
    def get_or_save(
        self,
        external_id: str,
        source: str,
        title: str,
        author: str,
        cover_url: str
    ) -> Book:
        ...
