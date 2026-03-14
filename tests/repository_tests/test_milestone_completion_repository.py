import pytest
from datetime import datetime, date

from app.domain.milestone_completion import MilestoneCompletion
from app.domain.milestone_type import MilestoneType
from app.persistence.sqlalchemy.tables import milestone_completions

from app.persistence.sqlalchemy.tables import milestone_types
from app.persistence.sqlalchemy.milestone_completion_repository_sqlalchemy import (
    MilestoneCompletionRepositorySQLAlchemy,
)
from app.domain.child import Child
from app.persistence.sqlalchemy.tables import children

@pytest.fixture
def clean_milestone_types(engine):
    with engine.begin() as conn:
        conn.execute(milestone_completions.delete())   # delete children first
        conn.execute(milestone_types.delete())         # then delete parent
    yield
    with engine.begin() as conn:
        conn.execute(milestone_completions.delete())
        conn.execute(milestone_types.delete())




@pytest.fixture
def child(engine):
    c = Child(
        id="child123",
        name="Test Child",
        date_of_birth=date(2018, 1, 1),  # valid date
        avatar_url=None,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    with engine.begin() as conn:
        conn.execute(children.insert().values(c.to_dict()))

    return c


class FakeMilestoneRepository:
    def __init__(self, milestone):
        self.milestone = milestone

    def get(self, milestone_id: str):
        return self.milestone if milestone_id == self.milestone.id else None


@pytest.fixture
def milestone(engine, clean_milestone_types):
    m = MilestoneType(
        name="Read 10 Books",
        type="reading",
        threshold=10,
        subject="reading",
        id="m1",
    )

    with engine.begin() as conn:
        conn.execute(milestone_types.insert().values(m.to_dict()))

    return m


@pytest.fixture
def repo(engine, milestone, child):
    fake_repo = FakeMilestoneRepository(milestone)
    return MilestoneCompletionRepositorySQLAlchemy(engine, fake_repo)


def test_save_and_get(repo, engine):
    mc = MilestoneCompletion(
        child_id="child123",
        milestone_id="m1",
        description="Completed reading milestone",
        completed_at=datetime.now(),
        reward_generated_at=None,
        reward_url=None,
    )

    # Base fields must be set manually
    mc.id = "c1"
    mc.created_at = datetime.now()
    mc.updated_at = datetime.now()

    repo.save(mc)

    fetched = repo.get("c1")

    assert fetched is not None
    assert fetched.id == mc.id
    assert fetched.child_id == mc.child_id
    assert fetched.milestone_id == mc.milestone_id
    assert isinstance(fetched.completed_at, datetime)


def test_get_all_by_child_and_key(repo, engine):
    now = datetime.now()

    mc1 = MilestoneCompletion(
        child_id="child123",
        milestone_id="m1",
        description="Reading milestone",
        completed_at=now,
        reward_generated_at=None,
        reward_url=None,
    )
    mc1.id = "mc1"
    mc1.created_at = now
    mc1.updated_at = now

    mc2 = MilestoneCompletion(
        child_id="child123",
        milestone_id="m1",
        description="Another reading milestone",
        completed_at=now,
        reward_generated_at=None,
        reward_url=None,
    )
    mc2.id = "mc2"
    mc2.created_at = now
    mc2.updated_at = now

    repo.save(mc1)
    repo.save(mc2)

    results = repo.get_all_by_child_and_key("child123", "reading")

    assert len(results) == 2
    assert all(mc.milestone_id == "m1" for mc in results)
    assert all(mc.child_id == "child123" for mc in results)