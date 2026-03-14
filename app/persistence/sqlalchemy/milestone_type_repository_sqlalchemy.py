#!/usr/bin/python3

from sqlalchemy import select
from sqlalchemy.engine import Engine

from app.domain.repositories.milestone_repository import MilestoneTypeRepositoryBase
from app.domain.milestone_type import MilestoneType

from app.persistence.sqlalchemy.tables import milestone_types


class MilestoneTypeRepositorySQLAlchemy(MilestoneTypeRepositoryBase):

    def __init__(self, engine: Engine):
        self.engine = engine

    def _to_domain(self, row) -> MilestoneType:
        return MilestoneType(
            id=row.id,
            name=row.name,
            subject=row.subject,
            type=row.type,
            threshold=row.threshold,
        )

    def get(self, id: str) -> MilestoneType | None:
        stmt = select(milestone_types).where(milestone_types.c.id == id)
        with self.engine.begin() as conn:
            result = conn.execute(stmt).first()

        if result is None:
            return None

        return self._to_domain(result)

    def get_all_by_type(self, milestone_type: str) -> list[MilestoneType]:
        stmt = select(milestone_types).where(milestone_types.c.type == milestone_type)
        with self.engine.begin() as conn:
            rows = conn.execute(stmt).fetchall()

        results = []

        for row in rows:
            domain_obj = self._to_domain(row)
            results.append(domain_obj)

        return results

    def get_by_threshold(self, threshold: int) -> MilestoneType | None:
        """ Expects that threshold values are unique in the Milestone table """
        stmt = select(milestone_types).where(milestone_types.c.threshold == threshold)
        with self.engine.begin() as conn:
            row = conn.execute(stmt).first()

        if row is None:
            return None

        return self._to_domain(row)

    def get_by_subject(self, subject: str | None) -> MilestoneType | None:
        """ Possibly useful for weekly goals? """
        stmt = select(milestone_types).where(milestone_types.c.subject == subject)
        with self.engine.begin() as conn:
            row = conn.execute(stmt).first()

        if row is None:
            return None

        return self._to_domain(row)

    def get_by_type_and_threshold(
        self,
        milestone_type: str,
        threshold: int
        ) -> MilestoneType | None:
        stmt = (
            select(milestone_types)
            .where(milestone_types.c.type == milestone_type)
            .where(milestone_types.c.threshold == threshold)
        )
        with self.engine.begin() as conn:
            row = conn.execute(stmt).first()

        if row is None:
            return None

        return self._to_domain(row)
