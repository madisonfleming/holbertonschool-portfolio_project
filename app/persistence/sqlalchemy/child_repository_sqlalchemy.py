#!/usr/bin/python3

from sqlalchemy import insert, select
from sqlalchemy.engine import Engine

from app.domain.repositories.child_repository import ChildRepositoryBase
from app.domain.child import Child
from app.persistence.sqlalchemy.tables import children


class ChildRepositorySQLAlchemy(ChildRepositoryBase):
    def __init__(self, engine: Engine):
        self.engine = engine

    def save(self, child: Child) -> Child:
        data = child.to_dict()

        """ open new db connection and run function. if:
        - no errors-> commit
        - error-> rollback
        then close connection """
        with self.engine.begin() as conn:
            stmt = insert(children).values(data) # SQL statement object
            conn.execute(stmt) # SQL run w/ above statement object
        return child

    def get(self, child_id: str) -> Child | None:
        with self.engine.connect() as conn:
            stmt = select(children).where(children.c.id == child_id)
            row = conn.execute(stmt).fetchone()

        if row is None:
            return None

        return Child.from_dict(dict(row._mapping))

    def get_by_ids(self, child_ids: list[str]) -> list[Child]:
        if not child_ids:
            return []

        with self.engine.connect() as conn:
            stmt = select(children).where(children.c.id.in_(child_ids))
            rows = conn.execute(stmt).fetchall()

        result = []
        for row in rows:
            child = Child.from_dict(row._mapping)
            result.append(child)
        
        return result
