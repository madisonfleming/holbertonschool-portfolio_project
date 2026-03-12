#!/usr/bin/python3

from sqlalchemy import insert, select
from sqlalchemy.engine import Engine

from app.domain.repositories.milestone_completion_repository import MilestoneCompletionRepositoryBase
from app.domain.milestone_completion import MilestoneCompletion
from app.persistence.sqlalchemy.tables import milestone_completions

from dataclasses import asdict
from datetime import datetime

"""
Note: update and delete not implemented
"""
class MilestoneCompletionRepositorySQLAlchemy(MilestoneCompletionRepositoryBase):
    def __init__(self, engine: Engine, milestone_repository):
        self.engine = engine
        self.milestone_repository = milestone_repository

    def save(self, milestone: MilestoneCompletion) -> MilestoneCompletion:
        with self.engine.begin() as conn:
            stmt = insert(milestone_completions).values(milestone.to_dict())
            conn.execute(stmt)
        return milestone

    def get(self, milestone_id: str) -> MilestoneCompletion | None:
        with self.engine.connect() as conn:
            stmt = select(milestone_completions).where(
                milestone_completions.c.id == milestone_id
            )
            row = conn.execute(stmt).fetchone()

        if row is None:
            return None

        return MilestoneCompletion.from_dict(row._mapping)

    def get_all_milestones_by_child(self, child_id: str) -> list[MilestoneCompletion]:
        with self.engine.connect() as conn:
            stmt = select(milestone_completions).where(
                milestone_completions.c.child_id == child_id
            )
            rows = conn.execute(stmt).fetchall()

        return [
            MilestoneCompletion.from_dict(row._mapping)
            for row in rows
        ]

    def get_all_by_child_and_key(
        self,
        child_id: str,
        milestone_key: str
    ) -> list[MilestoneCompletion]:
        with self.engine.connect() as conn:
            stmt = select(milestone_completions).where(
                milestone_completions.c.child_id == child_id
            )
            rows = conn.execute(stmt).fetchall()

        return [
            mc
            for mc in (MilestoneCompletion.from_dict(row._mapping) for row in rows)
            if self.milestone_repository.get(mc.milestone_id).type == milestone_key
        ]

    def get_most_recent_reading_milestone(
        self,
        child_id: str,
        type: str
    ) -> MilestoneCompletion | None:
        """ Used by create_reading_session to find a child's most recent milestone"""
        with self.engine.connect() as conn:
            stmt = select(milestone_completions).where(
                milestone_completions.c.child_id == child_id
            )
            rows = conn.execute(stmt).fetchall()

        completions = [
            MilestoneCompletion.from_dict(row._mapping)
            for row in rows
        ]

        filtered = [
            m for m in completions
            if self.milestone_repository.get(m.milestone_id).type == type
        ]

        if not filtered:
            return None

        most_recent = max(filtered, key=lambda mc: mc.created_at)
        return most_recent
