import pytest
from datetime import datetime
from sqlalchemy import create_engine, insert
from app.persistence.sqlalchemy.tables import milestone_types
from app.persistence.sqlalchemy.milestone_type_repository_sqlalchemy import (
    MilestoneTypeRepositorySQLAlchemy,
)


@pytest.fixture
def engine():
    # In-memory SQLite for fast, isolated tests
    engine = create_engine("sqlite:///:memory:", echo=False)
    milestone_types.create(engine)
    return engine


@pytest.fixture
def repo(engine):
    return MilestoneTypeRepositorySQLAlchemy(engine)


@pytest.fixture
def seed_data():
    now = datetime.now()

    return [
        {
            "id": "1",
            "name": "Read 25 Books",
            "subject": None,
            "type": "books_read",
            "threshold": 25,
            "created_at": now,
            "updated_at": now,
        },
        {
            "id": "2",
            "name": "Read 50 Books",
            "subject": None,
            "type": "books_read",
            "threshold": 50,
            "created_at": now,
            "updated_at": now,
        },
        {
            "id": "3",
            "name": "Read 5 Elephant Books",
            "subject": "elephants",
            "type": "weekly_goal",
            "threshold": 5,
            "created_at": now,
            "updated_at": now,
        },
    ]



def seed(engine, seed_data):
    with engine.begin() as conn:
        for row in seed_data:
            conn.execute(insert(milestone_types).values(**row))


# ---------------------------------------------------------
# GET BY ID
# ---------------------------------------------------------
def test_get_returns_correct_milestone(engine, repo, seed_data):
    seed(engine, seed_data)

    result = repo.get("1")

    assert result is not None
    assert result.id == "1"
    assert result.name == "Read 25 Books"


def test_get_returns_none_for_missing_id(repo):
    result = repo.get("999")
    assert result is None


# ---------------------------------------------------------
# GET ALL BY TYPE
# ---------------------------------------------------------
def test_get_all_by_type_returns_correct_items(engine, repo, seed_data):
    seed(engine, seed_data)

    results = repo.get_all_by_type("books_read")

    assert len(results) == 2

    ids = []
    for m in results:
        ids.append(m.id)

    assert "1" in ids
    assert "2" in ids


# ---------------------------------------------------------
# GET BY SUBJECT
# ---------------------------------------------------------
def test_get_by_subject_returns_correct_item(engine, repo, seed_data):
    seed(engine, seed_data)

    result = repo.get_by_subject("elephants")

    assert result is not None
    assert result.id == "3"
    assert result.subject == "elephants"


def test_get_by_subject_returns_none_when_missing(engine, repo, seed_data):
    seed(engine, seed_data)

    result = repo.get_by_subject("koalas")
    assert result is None


# ---------------------------------------------------------
# GET BY THRESHOLD
# ---------------------------------------------------------
def test_get_by_threshold_returns_correct_item(engine, repo, seed_data):
    seed(engine, seed_data)

    result = repo.get_by_threshold(50)

    assert result is not None
    assert result.id == "2"


def test_get_by_threshold_returns_none_when_missing(engine, repo, seed_data):
    seed(engine, seed_data)

    result = repo.get_by_threshold(999)
    assert result is None


# ---------------------------------------------------------
# GET BY TYPE + THRESHOLD
# ---------------------------------------------------------
def test_get_by_type_and_threshold_returns_correct_item(engine, repo, seed_data):
    seed(engine, seed_data)

    result = repo.get_by_type_and_threshold("books_read", 25)

    assert result is not None
    assert result.id == "1"


def test_get_by_type_and_threshold_returns_none_when_missing(engine, repo, seed_data):
    seed(engine, seed_data)

    result = repo.get_by_type_and_threshold("books_read", 999)
    assert result is None