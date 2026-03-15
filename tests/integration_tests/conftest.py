# Ensure test settings are applied first

import os
from app.config import get_settings

os.environ["ENVIRONMENT"] = "testing"
os.environ["DATABASE_URL"] = "sqlite+pysqlite:///./test.db"
# os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"
settings = get_settings()
print(settings)

import pytest
# Facade imports
from app.services.facade import MLBFacade

# DB imports
# from app.persistence.sqlalchemy.db import engine as engine
from sqlalchemy import create_engine, insert
from sqlalchemy.pool import StaticPool
from app.persistence.sqlalchemy.tables import metadata
from app.persistence.sqlalchemy.tables import users, children, relationships, books
from app.persistence.sqlalchemy.user_repository_sqlalchemy import UserRepositorySQLAlchemy
from app.persistence.sqlalchemy.child_repository_sqlalchemy import ChildRepositorySQLAlchemy
from app.persistence.sqlalchemy.reading_session_repository_sqlalchemy import ReadingSessionRepositorySQLAlchemy
from app.persistence.sqlalchemy.milestone_type_repository_sqlalchemy import MilestoneTypeRepositorySQLAlchemy
from app.persistence.sqlalchemy.milestone_completion_repository_sqlalchemy import MilestoneCompletionRepositorySQLAlchemy
from app.persistence.sqlalchemy.relationship_repository_sqlalchemy import RelationshipRepositorySQLAlchemy
from app.persistence.sqlalchemy.book_repository_sqlalchemy import BookRepositorySQLAlchemy
from app.external.open_library_api import OpenLibraryClient
from app.domain.user import User
from datetime import datetime, date

# FastAPI app imports
from fastapi.testclient import TestClient
from app.factory import create_app
from app.config import UnitTestingConfig
from app.api.auth_dependencies import auth_current_user
from app.api.dependencies import get_facade


engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


@pytest.fixture(autouse=True)
def setup_database():
    metadata.drop_all(bind=engine) 
    metadata.create_all(bind=engine)
    with engine.begin() as conn:
        stmt = insert(users).values(
            [
                {
                    "id": "123",
                    "name": "Alice",
                    "email": "alice@example.com",
                    "role": "standard",
                    "firebase_uid": "123",
                    "created_at": datetime.now(),
                    "updated_at": datetime.now()
                },
                {
                    "id": "777",
                    "name": "Bob",
                    "email": "bob@example.com",
                    "role": "standard",
                    "firebase_uid": "777",
                    "created_at": datetime.now(),
                    "updated_at": datetime.now()
                }
            ]
        )
        conn.execute(stmt)
        stmt = insert(children).values(
            [
                {
                    "id": "abc123",
                    "name": "Susie",
                    "date_of_birth": date(2020, 1, 1),
                    "avatar_url": None,
                    "created_at": datetime.now(),
                    "updated_at": datetime.now()
                }
            ]
        )
        conn.execute(stmt)
        stmt = insert(relationships).values(
            [
                {
                    "id": "rel123",
                    "user_id": "123",
                    "child_id": "abc123",
                    "role": "primary",
                    "relationship_type": "parent",
                    "invited_by": None,
                    "acceptance_status": "accepted",
                    "created_at": datetime.now(),
                    "updated_at": datetime.now()
                }
            ]
        )
        conn.execute(stmt)
        stmt = insert(books).values(
            [
                {
                    "id": "book123",
                    "external_id": "/works/OAM123",
                    "source": "openlibrary",
                    "title": "Where the Wild Things Are",
                    "author": "Maurice Sendak",
                    "cover_url": "/cover-wtwta",
                    "created_at": datetime.now(),
                    "updated_at": datetime.now()
                }
            ]
        )
        conn.execute(stmt)
    yield
    metadata.drop_all(bind=engine)


@pytest.fixture
def create_test_facade():
    milestone_repository = MilestoneTypeRepositorySQLAlchemy(engine) # create instance of type repo
    # create an instance of completion repo + pass in the type instance - Allows completion repo to use methods from type repo
    milestone_completion_repository = MilestoneCompletionRepositorySQLAlchemy(engine, milestone_repository)

    return MLBFacade(
        user_repository=UserRepositorySQLAlchemy(engine),
        child_repository=ChildRepositorySQLAlchemy(engine),
        reading_session_repository=ReadingSessionRepositorySQLAlchemy(engine),
        milestone_repository=milestone_repository,
        milestone_completion_repository=milestone_completion_repository,
        # milestone_repository=MilestoneTypeRepository(),
        # milestone_completion_repository=MilestoneCompletionRepository(),
        relationship_repository=RelationshipRepositorySQLAlchemy(engine),
        book_repository=BookRepositorySQLAlchemy(engine),
        open_library_api=OpenLibraryClient()
    )


@pytest.fixture
def app():
    app = create_app(UnitTestingConfig())
    app.dependency_overrides[auth_current_user] = lambda uid = "123": {"uid": uid }
    yield app
    app.dependency_overrides.clear()

@pytest.fixture
def client(create_test_facade, app):
    app.dependency_overrides[get_facade] = lambda: create_test_facade
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
