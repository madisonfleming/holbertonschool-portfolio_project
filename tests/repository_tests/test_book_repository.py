# tests/repository_tests/test_book_repository.py

from app.persistence.sqlalchemy.db import engine
from app.persistence.sqlalchemy.tables import books
from app.persistence.sqlalchemy.book_repository_sqlalchemy import BookRepositorySQLAlchemy
from app.domain.books import Book

from sqlalchemy import delete
from datetime import datetime, timezone
from uuid import uuid4
import pytest

# You can run this one repeatedly, has clean up
from app.persistence.sqlalchemy.tables import books

@pytest.fixture
def clean_books(engine):
    with engine.begin() as conn:
        conn.execute(books.delete())
    yield
    with engine.begin() as conn:
        conn.execute(books.delete())

def test_book_repository_crud(clean_books, engine):
    repo = BookRepositorySQLAlchemy(engine)

    book_id = str(uuid4())
    now = datetime.now()

    new_book = Book(
        id=book_id,
        external_id="OL123",
        source="openlibrary",
        title="Test Book",
        author="Test Author",
        cover_url="http://example.com/cover.jpg",
        created_at=now,
        updated_at=now,
    )

    # save
    print("Saving book...")
    with engine.begin() as conn:
        conn.execute(books.insert().values(new_book.to_dict()))

    # get
    print("Fetching book...")
    fetched = repo.get(book_id)
    assert fetched is not None
    assert fetched.id == book_id
    assert fetched.title == "Test Book"
    assert fetched.author == "Test Author"

    # search
    print("Searching for book...")
    results = repo.search("test")
    assert len(results) >= 1

    found = False
    for b in results:
        if b.id == book_id:
            found = True
            break

    assert found is True

    # get by external ID
    print("Fetching by external ID...")
    fetched_ext = repo.get_by_external_id("OL123", "openlibrary")
    assert fetched_ext is not None
    assert fetched_ext.id == book_id

    # clean it uup
    print("Deleting book...")
    with engine.begin() as conn:
        conn.execute(delete(books).where(books.c.id == book_id))

    print("Done.")

if __name__ == "__main__":
    test_book_repository_crud()
