import pytest
from sqlalchemy import text
from app.persistence.sqlalchemy.db import engine as real_engine
from app.persistence.sqlalchemy.tables import (
    milestone_completions,
    milestone_types,
    children,
)

@pytest.fixture(autouse=True)
def clean_database(engine):
    """Clean all dependent tables before each test, ignoring missing tables."""
    with engine.begin() as conn:
        for table in [milestone_completions, milestone_types, children]:
            try:
                conn.execute(table.delete())
            except Exception:
                pass

    yield

    # optional cleanup after test
    with engine.begin() as conn:
        for table in [milestone_completions, milestone_types, children]:
            try:
                conn.execute(table.delete())
            except Exception:
                pass


@pytest.fixture
def engine():
    return real_engine