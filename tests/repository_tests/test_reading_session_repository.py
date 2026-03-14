import pytest
from datetime import datetime
from uuid import uuid4

from sqlalchemy import create_engine, text

from app.domain.reading_sessions import ReadingSession
from app.persistence.sqlalchemy.tables import metadata, reading_sessions
from app.persistence.sqlalchemy.reading_session_repository_sqlalchemy import (
    ReadingSessionRepositorySQLAlchemy,
)


# ---------------------------------------------------------
# FIXTURES
# ---------------------------------------------------------

@pytest.fixture
def engine():
    engine = create_engine("sqlite:///:memory:", future=True)
    metadata.create_all(engine)
    return engine


@pytest.fixture
def repo(engine):
    return ReadingSessionRepositorySQLAlchemy(engine)


@pytest.fixture
def sample_session():
    now = datetime.now()
    return ReadingSession(
        id=None,
        child_id="child-123",
        external_id="ext-999",
        book_id="book-456",
        title="The Gruffalo",
        cover_url="http://example.com/gruffalo.jpg",
        logged_at=now,
        created_at=now,
        updated_at=now,
    )


# ---------------------------------------------------------
# TESTS
# ---------------------------------------------------------

def test_save_inserts_new_session(repo, engine, sample_session):
    saved = repo.save(sample_session)

    # ID + timestamps should be set
    assert saved.id is not None
    assert saved.created_at is not None
    assert saved.updated_at is not None

    # Verify DB row exists
    with engine.begin() as conn:
        row = conn.execute(
            text("SELECT * FROM ReadingSession WHERE id = :id"),
            {"id": saved.id},
        ).mappings().fetchone()

    assert row is not None
    assert row["child_id"] == "child-123"
    assert row["external_id"] == "ext-999"
    assert row["book_id"] == "book-456"
    assert row["title"] == "The Gruffalo"


def test_get_by_id_returns_correct_session(repo, sample_session):
    saved = repo.save(sample_session)

    fetched = repo.get_by_id(saved.id)

    assert fetched is not None
    assert fetched.id == saved.id
    assert fetched.child_id == saved.child_id
    assert fetched.book_id == saved.book_id
    assert fetched.title == saved.title


def test_get_by_id_returns_none_when_missing(repo):
    result = repo.get_by_id("does-not-exist")
    assert result is None


def test_get_by_child_returns_all_matching(repo, sample_session):
    # First session
    s1 = repo.save(sample_session)

    # Second session for same child
    now = datetime.now()
    s2 = ReadingSession(
        id=None,
        child_id=sample_session.child_id,
        external_id="ext-222",
        book_id="book-789",
        title="Bluey",
        cover_url=None,
        logged_at=now,
        created_at=now,
        updated_at=now,
    )
    repo.save(s2)

    results = repo.get_by_child(sample_session.child_id)

    assert len(results) == 2
    ids = {r.id for r in results}
    assert s1.id in ids
    assert s2.id in ids


def test_get_by_child_returns_empty_list_when_none(repo):
    results = repo.get_by_child("no-such-child")
    assert results == []


def test_update_modifies_existing_row(repo, engine, sample_session):
    saved = repo.save(sample_session)

    # Modify fields
    saved.title = "The Gruffalo (Updated)"
    saved.cover_url = "http://example.com/new.jpg"

    updated = repo.update(saved)

    assert updated.updated_at > updated.created_at

    # Verify DB row updated
    with engine.begin() as conn:
        row = conn.execute(
            text("SELECT * FROM ReadingSession WHERE id = :id"),
            {"id": saved.id},
        ).mappings().fetchone()

    assert row["title"] == "The Gruffalo (Updated)"
    assert row["cover_url"] == "http://example.com/new.jpg"