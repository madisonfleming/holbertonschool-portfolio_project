import pytest
# Facade imports
from app.services.facade import MLBFacade
from app.persistence.user_repository import UserRepository
from app.persistence.child_repository import ChildRepository
from app.persistence.reading_session_repository import ReadingSessionRepository
from app.persistence.milestone_repository import MilestoneTypeRepository
from app.persistence.milestone_completion_repository import MilestoneCompletionRepository
from app.persistence.relationship_repository import RelationshipRepository
from app.persistence.book_repository import BookRepository
from app.external.open_library_api import OpenLibraryClient

# FastAPI app imports
from fastapi.testclient import TestClient
from app.factory import create_app
from app.config import UnitTestingConfig
from app.api.auth_dependencies import auth_current_user
from app.api.dependencies import get_facade

@pytest.fixture
def create_test_facade():
    return MLBFacade(
        user_repository=UserRepository(),
        child_repository=ChildRepository(),
        reading_session_repository=ReadingSessionRepository(),
        milestone_repository=MilestoneTypeRepository(),
        milestone_completion_repository=MilestoneCompletionRepository(),
        relationship_repository=RelationshipRepository(),
        book_repository=BookRepository(),
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
