#!/usr/bin/python3

from app.domain.repositories.book_repository import BookRepositoryBase
from app.domain.books import Book
from app.persistence.in_memory_seed import Bookdata

from datetime import datetime
from uuid import uuid4

class BookRepository(BookRepositoryBase):
    def __init__(self):     # this is here to accommodate seed data
        self._storage = {}
        now = datetime.now()

        for book in Bookdata().books.values():
            self._storage[book.id] = {
                "id": book.id,
                "external_id": book.external_id,
                "source": book.source,
                "title": book.title,
                "author": book.author,
                "cover_url": book.cover_url,
                "created_at": now.isoformat(),
                "updated_at": now.isoformat(),
            }


    # returns results for the local DB
    def search(
        self,
        query: str,
        subjects: list[str] | None = None,
        limit: int | None = None
    ) -> list[Book] | None:
        results = []

        for book in self._storage.values():
            title = book["title"]
            if query.lower() in book["title"].lower():     # convert to lowercase for flex matching
                results.append(Book.from_dict(book))

        return results[:limit] if limit else results

    # retrieve a book by its internal ID
    def get(self, book_id: str) -> Book | None:
        data = self._storage.get(book_id)
        if not data:
            return None
        return Book.from_dict(data)

    # retrieve a book by external ID from ext API
    def get_by_external_id(
        self,
        external_id: str,
        source: str
    ) -> Book | None:
        for book in self._storage.values():
            if book["external_id"] == external_id and book["source"] == source:
                return Book.from_dict(book)
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

        now = datetime.now()

        # create new book if not exists
        new_book = Book(
            id=str(uuid4()),            # freshie internal book_id
            external_id=external_id,
            source=source,
            title=title,
            author=author,
            cover_url=cover_url,
            created_at=now,
            updated_at=now,
        )

        # save to db w/ book_id as key and new_book details applied
        self._storage[new_book.id] = new_book.to_dict()
        return new_book
