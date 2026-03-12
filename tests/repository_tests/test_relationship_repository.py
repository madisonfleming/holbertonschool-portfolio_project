import pytest
from datetime import datetime, date
from sqlalchemy import create_engine, text

from app.persistence.sqlalchemy.tables import (
    metadata,
    users,
    children,
    relationships,
)
from app.persistence.sqlalchemy.relationship_repository_sqlalchemy import (
    RelationshipRepositorySQLAlchemy,
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
    return RelationshipRepositorySQLAlchemy(engine)


@pytest.fixture
def seed_user_and_child(engine):
    with engine.begin() as conn:
        conn.execute(
            users.insert().values(
                id="user-1",
                name="Mel",
                email="mel@example.com",
                role="standard",
                firebase_uid="firebase-1",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
        )

        conn.execute(
            children.insert().values(
                id="child-1",
                name="Kiddo",
                date_of_birth=date(2015, 1, 1),   # ✔ FIXED
                avatar_url=None,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
        )


# ---------------------------------------------------------
# TESTS
# ---------------------------------------------------------

def test_create_relationship(repo, engine, seed_user_and_child):
    rel_id = repo.create_relationship(
        user_id="user-1",
        child_id="child-1",
        role="primary",
        relationship_type="Parent",
    )

    with engine.begin() as conn:
        row = conn.execute(
            text("SELECT * FROM Relationship WHERE id = :id"),
            {"id": rel_id},
        ).mappings().fetchone()

    assert row is not None
    assert row["user_id"] == "user-1"
    assert row["child_id"] == "child-1"
    assert row["role"] == "primary"
    assert row["relationship_type"] == "Parent"
    assert row["acceptance_status"] == "accepted"


def test_get(repo, seed_user_and_child):
    rel_id = repo.create_relationship("user-1", "child-1", "primary", "Parent")

    result = repo.get(rel_id)

    assert result is not None
    assert result["id"] == rel_id
    assert result["role"] == "primary"


def test_get_returns_none(repo):
    assert repo.get("missing") is None


def test_get_relationship_type(repo, seed_user_and_child):
    repo.create_relationship("user-1", "child-1", "primary", "Parent")

    result = repo.get_relationship_type("user-1", "child-1")

    assert result is not None
    assert result["relationship_type"] == "Parent"


def test_get_relationship_type_returns_none(repo):
    assert repo.get_relationship_type("nope", "nope") is None


def test_has_role(repo, seed_user_and_child):
    repo.create_relationship("user-1", "child-1", "primary", "Parent")

    assert repo.has_role("user-1", "child-1", "primary") is True
    assert repo.has_role("user-1", "child-1", "secondary") is False


def test_has_one_of_roles(repo, seed_user_and_child):
    repo.create_relationship("user-1", "child-1", "primary", "Parent")

    assert repo.has_one_of_roles("user-1", "child-1", ["secondary", "primary"]) is True
    assert repo.has_one_of_roles("user-1", "child-1", ["secondary"]) is False


def test_has_relationship(repo, seed_user_and_child):
    repo.create_relationship("user-1", "child-1", "primary", "Parent")

    assert repo.has_relationship("user-1", "child-1") is True
    assert repo.has_relationship("user-1", "child-999") is False


def test_get_children_per_user(repo, seed_user_and_child):
    repo.create_relationship("user-1", "child-1", "primary", "Parent")

    results = repo.get_children_per_user("user-1")

    assert len(results) == 1
    assert results[0]["child_id"] == "child-1"