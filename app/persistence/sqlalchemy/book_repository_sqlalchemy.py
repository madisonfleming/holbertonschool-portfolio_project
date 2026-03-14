#!/usr/bin/python3

from sqlalchemy import insert, select
from sqlalchemy.engine import Engine

from app.domain.repositories.book_repository import BookRepositoryBase
from app.domain.books import Book
from app.persistence.sqlalchemy.db import engine
from app.persistence.sqlalchemy.tables import books

from datetime import datetime
from uuid import uuid4

class BookRepositorySQLAlchemy(BookRepositoryBase):
    def __init__(self, engine: Engine = engine):
        self.engine = engine

    # returns results for the local DB
    def search(
        self,
        query: str,
        subjects: list[str] | None = None,
        limit: int | None = None
    ) -> list[Book] | None:

        with self.engine.connect() as conn:
            stmt = select(books).where(books.c.title.ilike(f"%{query}%")) # ilike is case-insensitive
            rows = conn.execute(stmt).fetchall()

        results = []
        for row in rows:
            book = Book.from_dict(row._mapping)
            results.append(book)

        return results[:limit] if limit else results

    def get(self, book_id: str) -> Book | None:
        with self.engine.connect() as conn:
            stmt = select(books).where(books.c.id == book_id)
            row = conn.execute(stmt).fetchone()

        if row is None:
            return None

        return Book.from_dict(row._mapping)

    # retrieve a book by external ID from ext API
    def get_by_external_id(
        self,
        external_id: str,
        source: str
    ) -> Book | None:
        with self.engine.connect() as conn:
            stmt = select(books).where(
                books.c.external_id == external_id,
                books.c.source == source
            )
            row = conn.execute(stmt).fetchone()

        if row is None:
            return None

        return Book.from_dict(row._mapping)

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
        with self.engine.begin() as conn:
            insert_stmt = insert(books).values(new_book.to_dict())
            conn.execute(insert_stmt)

        return new_book
