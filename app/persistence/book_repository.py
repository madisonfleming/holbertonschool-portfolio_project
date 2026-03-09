#!/usr/bin/python3

from app.domain.repositories.book_repository import BookRepositoryBase
from app.domain.books import Book
from app.persistence.in_memory_seed import Bookdata

from uuid import uuid4

class BookRepository(BookRepositoryBase):
    def __init__(self):
        self._storage = Bookdata().books


    # returns results for the local DB
    def search(
        self,
        query: str,
        subjects: list[str] | None = None,
        limit: int | None = None
    ) -> Book | None:
        results = []

        # match titles
        for book in self._storage.values():
            if query.lower() in book.title.lower():     # convert to lowercase for flex matching
                results.append(book)
        
        return results[:limit] if limit else results


    # retrieve a book by its internal ID
    def get(self, book_id: str) -> Book | None:
        return self._storage.get(book_id)


    # retrieve a book by external ID from ext API
    def get_by_external_id(self, external_id: str, source: str) -> Book | None:
        for book in self._storage.values():
            if book.external_id == external_id and book.source == source:
                return book
        return None


    # save book details to the DB if not existing
    def get_or_save(
        self,
        external_id: str,
        source: str,
        title: str,
        author: str,
        cover_url: str
    ) -> Book:
        # check if book exists in db
        existing = self.get_by_external_id(external_id, source)
        if existing:
            return existing

        # create new book if not exists
        new_book = Book(
            id=str(uuid4()),            # freshie internal book_id
            external_id=external_id,
            source=source,
            title=title,
            author=author,
            cover_url=cover_url,
        )

        # save to db w/ book_id as key and new_book details applied
        self._storage[new_book.id] = new_book
        return new_book
