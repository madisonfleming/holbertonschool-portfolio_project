from datetime import datetime
from uuid import uuid4

from sqlalchemy import select, insert, update
from sqlalchemy.engine import Engine

from app.domain.reading_sessions import ReadingSession
from app.domain.repositories.reading_session_repository import ReadingSessionRepositoryBase
from app.persistence.sqlalchemy.tables import reading_sessions


class ReadingSessionRepositorySQLAlchemy(ReadingSessionRepositoryBase):
    def __init__(self, engine: Engine):
        self.engine = engine

    def save(self, session: ReadingSession) -> ReadingSession:
        now = datetime.now()

        if session.id is None:
            session.id = str(uuid4())
            session.created_at = now

        session.updated_at = now

        with self.engine.begin() as conn:
            stmt = insert(reading_sessions).values(session.to_dict())
            conn.execute(stmt)

        return session


    def get_by_id(self, id: str) -> ReadingSession | None:
        stmt = select(reading_sessions).where(reading_sessions.c.id == id)
        with self.engine.begin() as conn:
            row = conn.execute(stmt).mappings().fetchone()

        if row is None:
            return None

        return ReadingSession.from_dict(dict(row))

    def get_by_child(self, child_id: str) -> list[ReadingSession]:
        stmt = select(reading_sessions).where(
            reading_sessions.c.child_id == child_id
        )

        with self.engine.begin() as conn:
            rows = conn.execute(stmt).mappings().fetchall()

        results = []
        for row in rows:
            results.append(ReadingSession.from_dict(dict(row)))

        return results


    def update(self, session: ReadingSession) -> ReadingSession:
        now = datetime.now()
        session.updated_at = now

        with self.engine.begin() as conn:
            stmt = (
                update(reading_sessions)
                .where(reading_sessions.c.id == session.id)
                .values(session.to_dict())
            )
            conn.execute(stmt)

        return session