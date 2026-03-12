import pytest
from datetime import date

from app.domain.child import Child
from app.persistence.sqlalchemy.child_repository_sqlalchemy import ChildRepositorySQLAlchemy
from app.persistence.sqlalchemy.tables import children


@pytest.fixture
def repo(engine):
    """Create a fresh repository instance for each test."""
    return ChildRepositorySQLAlchemy(engine)


@pytest.fixture
def clean_children_table(engine):
    """Ensure the children table is empty before each test."""
    with engine.begin() as conn:
        conn.execute(children.delete())
    yield
    # optional cleanup after test
    with engine.begin() as conn:
        conn.execute(children.delete())


def test_child_repository_crud(repo, clean_children_table):
    # Create a child domain object
    child = Child(
        id="test123",
        name="Test Child",
        date_of_birth=date(2015, 1, 1),
    )

    # Save the child
    repo.save(child)

    # Fetch it back
    fetched = repo.get("test123")

    # Assertions
    assert fetched is not None
    assert fetched.id == "test123"
    assert fetched.name == "Test Child"
    assert fetched.date_of_birth == date(2015, 1, 1)


def test_get_by_ids(repo, clean_children_table):
    child1 = Child(id="c1", name="Alpha", date_of_birth=date(2014, 5, 5))
    child2 = Child(id="c2", name="Beta", date_of_birth=date(2016, 7, 7))

    repo.save(child1)
    repo.save(child2)

    results = repo.get_by_ids(["c1", "c2"])

    assert len(results) == 2
    ids = {c.id for c in results}
    assert ids == {"c1", "c2"}