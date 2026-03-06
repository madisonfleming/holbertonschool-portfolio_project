"""
This file defines a FakeFacade class and the fixtures shared by the API test files
"""
import pytest
from fastapi.testclient import TestClient
from app.factory import create_app
from app.config import UnitTestingConfig
from app.api.dependencies import get_facade
from app.api.auth_dependencies import auth_current_user
from app.services.exceptions import RelationshipNotFoundError, PermissionDeniedError, ReadingSessionNotFoundError, DuplicateUserError
from app.domain.exceptions import UserNotFoundError

class FakeFacade:
    """ 
    Add facade mocks here 

    - Use dot notation in the return data to match pydantic models
    """
    def create_child(self, child_data, firebase_uid="123"):
        return {
            "id": "test-child-id",
            "name": child_data.name,
            "date_of_birth": child_data.date_of_birth,
            "age": 2,
            "avatar_url": child_data.avatar_url,
            "relationship_type": child_data.relationship_type or "Parent",
            "role": "primary"
        }
    def get_children(self, firebase_uid):
        if firebase_uid == "123":
            return [
                {
                    "id": "test-child-id-2",
                    "name": "Susie",
                    "age": 2,
                    "avatar_url": None,
                    "relationship_type": "Parent",
                    "role": "primary"
                },
                {
                    "id": "test-child-id-3",
                    "name": "Billy",
                    "age": 1,
                    "avatar_url": None,
                    "relationship_type": "Parent",
                    "role": "primary"
                }]
        if firebase_uid == "777":
            return []

    def get_child(self, child_id, firebase_uid):
        if firebase_uid == "123" and child_id == "test-child-id-2":
            return {
                "id": "test-child-id-2",
                "name": "Susie",
                "age": 2,
                "avatar_url": None,
                "relationship_type": "Parent",
                "role": "primary"
                }
        if firebase_uid == "777":
            raise RelationshipNotFoundError("777", "test-child-id-2") # this should catch before ChildNotFoundError() in real facade

    def update_child(self, child_id, child_data, firebase_uid):
        if firebase_uid == "123" and child_id == "test-child-id-2":
            return {
                "id": "test-child-id-2",
                "name": "Suzanne",
                "age": 2,
                "avatar_url": "alien_avatar.com",
                "relationship_type": "Parent",
                "role": "primary"
            }
        if firebase_uid == "777":
            raise RelationshipNotFoundError("777", "test-child-id-2")
        
    def create_reading_session(self, reading_session_data, firebase_uid):
        return {
            "session_id": "test-session-id",
            "child_id": reading_session_data.child_id,
            "book_id": "test-book-id",
            "logged_at": "2025-02-26T10:00:00",
        }

    def get_reading_sessions(self, child_id, firebase_uid, limit=None, from_date=None, to_date=None):
        if firebase_uid == "123" and child_id == "test-child-id-2":
            return [
                {
                    "session_id": "test-session-id-1",
                    "child_id": "test-child-id-2",
                    "book_id": "test-book-id-1",
                    "logged_at": "2025-02-26T10:00:00",
                },
                {
                    "session_id": "test-session-id-2",
                    "child_id": "test-child-id-2",
                    "book_id": "test-book-id-2",
                    "logged_at": "2025-01-15T09:00:00",
                },
            ]
        if firebase_uid == "777":
            raise PermissionDeniedError()  # "Insufficient permissions to complete this action"
        if firebase_uid == "123" and child_id == "test-child-id-empty":
            return []

    def update_session(self, session_id, updated_session_data, firebase_uid):
        if firebase_uid == "123" and session_id == "test-session-id-1":
            return {
                "session_id": "test-session-id-1",
                "child_id": "test-child-id-2",
                "book_id": updated_session_data.book_id or "test-book-id-1",
                "logged_at": updated_session_data.logged_at or "2025-02-26T10:00:00",
            }
        if firebase_uid == "777":
            raise PermissionDeniedError()  # "Insufficient permissions to complete this action"
        if session_id == "nonexistent-session-id":
            raise ReadingSessionNotFoundError(session_id)  # "Reading session with id: 'nonexistent-session-id' not found"

    def count_reading_sessions(self, child_id, firebase_uid, from_date=None, to_date=None):
        if firebase_uid == "123" and child_id == "test-child-id-2":
            return 5
        if firebase_uid == "123" and child_id == "test-child-id-empty":
            return 0
        if firebase_uid == "777":
            raise PermissionDeniedError()  # "Insufficient permissions to complete this action"

    def get_user(self, firebase_uid):
        if firebase_uid == "123":
            return {
                "id": "a686c824-25e6-4704-87a6-651938429111",
                "name": "Mary",
                "email": "mary@example.com",
                "role": "standard",
                }
        else:
            raise UserNotFoundError()

    def update_user(self, request, firebase_uid):
        if firebase_uid == "123" and request.email != "john@example.com":
            return {
                "id": "a686c824-25e6-4704-87a6-651938429111",
                "name": request.name or "Mary",
                "email": request.email or "mary@example.com",
                "role": "standard"
                }
        if firebase_uid == "123" and request.email == "john@example.com":
            raise DuplicateUserError()
        else:
            raise UserNotFoundError()        
    

# app with Facade dependency override (auth overrides are done per test)
@pytest.fixture
def test_app(monkeypatch):
    # Ensures that the test's uid override happens before the auth_current_user's override
    monkeypatch.setenv("ENVIRONMENT", "testing")

    app = create_app(settings=UnitTestingConfig())

    app.dependency_overrides[get_facade] = lambda: FakeFacade()
    yield app
    app.dependency_overrides.clear()

@pytest.fixture
def client(test_app):
    return TestClient(test_app)

#Allow dynamic uid creation for auth dependency overrides
@pytest.fixture
def override_auth(test_app):
    def _override(uid: str):
        async def override():
            return {"uid" : uid}
        test_app.dependency_overrides[auth_current_user] = override
    return _override