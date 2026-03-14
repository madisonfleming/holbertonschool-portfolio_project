from sqlalchemy import insert, select, update
from sqlalchemy.engine import Engine

from app.domain.user import User
from app.domain.repositories.user_repository import UserRepositoryBase
from app.persistence.sqlalchemy.tables import users  # your SQLAlchemy User table

from datetime import datetime

class UserRepositorySQLAlchemy(UserRepositoryBase):
    def __init__(self, engine: Engine):
        self.engine = engine

    def save(self, user: User) -> None:
        with self.engine.begin() as conn:
            stmt = insert(users).values(user.to_dict())
            conn.execute(stmt)

    def get(self, user_id: str) -> User | None:
        stmt = select(users).where(users.c.id == user_id)
        with self.engine.begin() as conn:
            row = conn.execute(stmt).mappings().fetchone()

        if row is None:
            return None

        return User.from_dict(row)

    def get_by_firebase_uid(self, firebase_uid: str) -> User | None:
        stmt = select(users).where(users.c.firebase_uid == firebase_uid)
        with self.engine.begin() as conn:
            row = conn.execute(stmt).mappings().fetchone()

        if row is None:
            return None

        return User.from_dict(row)

    # returns a user obj by email address (if found)
    # filtering is completed in SQL
    def get_by_email(self, email: str) -> User | None:
        stmt = select(users).where(users.c.email.ilike(email))
        with self.engine.begin() as conn:
            row = conn.execute(stmt).mappings().fetchone()

        if row is None:
            return None

        return User.from_dict(row)

    def update(self, user: User) -> None:
        with self.engine.begin() as conn:
            stmt = (
                update(users)
                .where(users.c.id == user.id)
                .values(
                    name=user.name,
                    email=user.email,
                    role=user.role,
                    firebase_uid=user.firebase_uid,
                    updated_at=datetime.now(),
                )
            )
            conn.execute(stmt)
