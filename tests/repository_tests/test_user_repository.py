import pytest
from datetime import datetime
from sqlalchemy import create_engine, text

from app.domain.user import User
from app.persistence.sqlalchemy.tables import metadata, users
from app.persistence.sqlalchemy.user_repository_sqlalchemy import (
    UserRepositorySQLAlchemy,
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
    return UserRepositorySQLAlchemy(engine)


@pytest.fixture
def sample_user():
    now = datetime.now()
    return User(
        id="user-123",
        name="Mel",
        email="mel@example.com",
        role="standard",
        firebase_uid="firebase-abc",
        created_at=now,
        updated_at=now,
    )


# ---------------------------------------------------------
# TESTS
# ---------------------------------------------------------

def test_save_inserts_user(repo, engine, sample_user):
    repo.save(sample_user)

    with engine.begin() as conn:
        row = conn.execute(
            text("SELECT * FROM User WHERE firebase_uid = :uid"),
            {"uid": sample_user.firebase_uid},
        ).mappings().fetchone()

    assert row is not None
    assert row["id"] == "user-123"
    assert row["name"] == "Mel"
    assert row["email"] == "mel@example.com"
    assert row["role"] == "standard"
    assert row["firebase_uid"] == "firebase-abc"


def test_get_returns_correct_user(repo, sample_user):
    repo.save(sample_user)

    fetched = repo.get("user-123")

    assert fetched is not None
    assert fetched.id == "user-123"
    assert fetched.name == "Mel"
    assert fetched.email == "mel@example.com"
    assert fetched.role == "standard"
    assert fetched.firebase_uid == "firebase-abc"


def test_get_returns_none_when_missing(repo):
    assert repo.get("missing-id") is None


def test_get_by_firebase_uid(repo, sample_user):
    repo.save(sample_user)

    fetched = repo.get_by_firebase_uid("firebase-abc")

    assert fetched is not None
    assert fetched.id == "user-123"
    assert fetched.email == "mel@example.com"


def test_get_by_firebase_uid_returns_none(repo):
    assert repo.get_by_firebase_uid("nope") is None


def test_get_by_email_exact_match(repo, sample_user):
    repo.save(sample_user)

    fetched = repo.get_by_email("mel@example.com")

    assert fetched is not None
    assert fetched.id == "user-123"


def test_get_by_email_case_insensitive(repo, sample_user):
    repo.save(sample_user)

    fetched = repo.get_by_email("MEL@EXAMPLE.COM")

    assert fetched is not None
    assert fetched.firebase_uid == "firebase-abc"


def test_get_by_email_returns_none(repo):
    assert repo.get_by_email("missing@example.com") is None