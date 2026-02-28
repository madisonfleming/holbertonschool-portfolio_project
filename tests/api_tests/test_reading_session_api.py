"""
These tests call the /reading-sessions and /children/{child_id}/reading-sessions endpoints

Validates that each method on the endpoint:
  - accepts a valid request payload
  - validates the payload using a Pydantic input model
  - calls the facade layer, delegating business logic to the facade
  - returns a response that matches the expected Pydantic response
    schema

Note that the facade layer is mocked - does not test business logic
or data persistence

"""

from fastapi.testclient import TestClient
from app.factory import create_app
from app.config import UnitTestingConfig
from app.api.dependencies import get_facade
from app.api.auth_dependencies import auth_current_user
from app.services.exceptions import RelationshipNotFoundError, PermissionDeniedError, ReadingSessionNotFoundError
import pytest


class FakeFacade:
    """
    Add facade mocks here

    - Use dot notation in the return data to match pydantic models
    """

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


# app with Facade dependency override (auth overrides are done per test)
@pytest.fixture
def app():
    app = create_app(UnitTestingConfig())
    app.dependency_overrides[get_facade] = lambda: FakeFacade()
    yield app
    app.dependency_overrides.clear()


@pytest.fixture
def client(app):
    return TestClient(app)


# Allow dynamic uid creation for auth dependency overrides
@pytest.fixture
def override_auth(app):
    def _override(uid: str):
        async def override():
            return {"uid": uid}
        app.dependency_overrides[auth_current_user] = override
    return _override


# Set the env to "testing"
@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "testing")


SESSIONS_BASE_URL = "/api/reading-sessions"
CHILDREN_BASE_URL = "/api/children"


# <--- CREATE READING SESSION TESTS --->

# Happy Path: test 201 reading session created successfully
def test_create_reading_session(client, override_auth):
    override_auth("123")
    payload = {
        "child_id": "test-child-id-2",
        "external_id": "OL123M",
        "source": "openlibrary",
        "title": "The Very Hungry Caterpillar",
        "author": "Eric Carle",
        "cover_url": "https://covers.openlibrary.org/b/id/123-M.jpg",
        "logged_at": "2025-02-26T10:00:00",
    }
    response = client.post(SESSIONS_BASE_URL, json=payload)
    assert response.status_code == 201
    assert response.json()["session_id"] == "test-session-id"
    assert response.json()["child_id"] == "test-child-id-2"
    assert response.json()["book_id"] == "test-book-id"
    assert response.json()["logged_at"] is not None


# Negative Path: test 400 (child_id missing) raises custom RequestValidationError
def test_create_reading_session_missing_child_id(client, override_auth):
    override_auth("123")
    payload = {
        "external_id": "OL123M",
        "source": "openlibrary",
        "title": "The Very Hungry Caterpillar",
        "author": "Eric Carle",
        "cover_url": "https://covers.openlibrary.org/b/id/123-M.jpg",
        "logged_at": "2025-02-26T10:00:00",
    }
    response = client.post(SESSIONS_BASE_URL, json=payload)
    assert response.status_code == 400
    assert response.json()["error"] == "VALIDATION_ERROR"
    assert "('body', 'child_id')" in response.json()["message"]
    assert response.json()["status"] == 400


# Negative Path: test 400 (logged_at missing) raises custom RequestValidationError
def test_create_reading_session_missing_logged_at(client, override_auth):
    override_auth("123")
    payload = {
        "child_id": "test-child-id-2",
        "external_id": "OL123M",
        "source": "openlibrary",
        "title": "The Very Hungry Caterpillar",
        "author": "Eric Carle",
        "cover_url": "https://covers.openlibrary.org/b/id/123-M.jpg",
    }
    response = client.post(SESSIONS_BASE_URL, json=payload)
    assert response.status_code == 400
    assert response.json()["error"] == "VALIDATION_ERROR"
    assert "('body', 'logged_at')" in response.json()["message"]
    assert response.json()["status"] == 400


# Negative Path: test 400 (invalid logged_at format) raises custom RequestValidationError
def test_create_reading_session_invalid_logged_at(client, override_auth):
    override_auth("123")
    payload = {
        "child_id": "test-child-id-2",
        "external_id": "OL123M",
        "source": "openlibrary",
        "title": "The Very Hungry Caterpillar",
        "author": "Eric Carle",
        "cover_url": "https://covers.openlibrary.org/b/id/123-M.jpg",
        "logged_at": "26-02-2025",  # invalid format
    }
    response = client.post(SESSIONS_BASE_URL, json=payload)
    assert response.status_code == 400
    assert response.json()["error"] == "VALIDATION_ERROR"
    assert "('body', 'logged_at')" in response.json()["message"]
    assert response.json()["status"] == 400


# Negative Path: test 401 unauthorised user - no auth override
def test_create_reading_session_as_unauthorised_user(client):
    payload = {
        "child_id": "test-child-id-2",
        "external_id": "OL123M",
        "source": "openlibrary",
        "title": "The Very Hungry Caterpillar",
        "author": "Eric Carle",
        "cover_url": "https://covers.openlibrary.org/b/id/123-M.jpg",
        "logged_at": "2025-02-26T10:00:00",
    }
    response = client.post(SESSIONS_BASE_URL, json=payload)
    assert response.status_code == 401
    assert response.json()["status"] == 401
    assert response.json()["error"] == "Not authenticated"
    assert response.json()["message"] == "Not authenticated"


# <--- GET READING SESSIONS TESTS --->

# Happy Path: test 200 success with sessions returned
def test_get_reading_sessions_with_data(client, override_auth):
    override_auth("123")
    response = client.get(f"{CHILDREN_BASE_URL}/test-child-id-2/reading-sessions")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    assert response.json()[0]["session_id"] == "test-session-id-1"
    assert response.json()[0]["child_id"] == "test-child-id-2"
    assert response.json()[0]["book_id"] == "test-book-id-1"
    assert response.json()[0]["logged_at"] is not None

    assert response.json()[1]["session_id"] == "test-session-id-2"
    assert response.json()[1]["child_id"] == "test-child-id-2"
    assert response.json()[1]["book_id"] == "test-book-id-2"


# Happy Path: test 200 success with no sessions returned (empty list)
def test_get_reading_sessions_without_data(client, override_auth):
    override_auth("123")
    response = client.get(f"{CHILDREN_BASE_URL}/test-child-id-empty/reading-sessions")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json() == []


# Negative Path: test 403 user has no permission for this child
def test_get_reading_sessions_without_permission(client, override_auth):
    override_auth("777")
    response = client.get(f"{CHILDREN_BASE_URL}/test-child-id-2/reading-sessions")
    assert response.status_code == 403
    assert response.json()["status"] == 403
    assert response.json()["error"] == "PERMISSION_DENIED"
    assert response.json()["message"] == "Insufficient permissions to complete this action"


# Negative Path: test 401 unauthorised user - no auth override
def test_get_reading_sessions_as_unauthorised_user(client):
    response = client.get(f"{CHILDREN_BASE_URL}/test-child-id-2/reading-sessions")
    assert response.status_code == 401
    assert response.json()["status"] == 401
    assert response.json()["error"] == "Not authenticated"
    assert response.json()["message"] == "Not authenticated"


# <--- UPDATE READING SESSION TESTS --->

# Happy Path: test 200 success update book_id on a session
def test_update_reading_session(client, override_auth):
    override_auth("123")
    payload = {
        "book_id": "updated-book-id",
        "logged_at": "2025-03-01T08:30:00",
    }
    response = client.put(f"{SESSIONS_BASE_URL}/test-session-id-1", json=payload)
    assert response.status_code == 200
    assert response.json()["session_id"] == "test-session-id-1"
    assert response.json()["book_id"] == "updated-book-id"
    assert response.json()["logged_at"] is not None


# Negative Path: test 400 (invalid logged_at format) raises custom RequestValidationError
def test_update_reading_session_invalid_logged_at(client, override_auth):
    override_auth("123")
    payload = {
        "logged_at": "01-03-2025",  # invalid format
    }
    response = client.put(f"{SESSIONS_BASE_URL}/test-session-id-1", json=payload)
    assert response.status_code == 400
    assert response.json()["error"] == "VALIDATION_ERROR"
    assert "('body', 'logged_at')" in response.json()["message"]
    assert response.json()["status"] == 400


# Negative Path: test 403 user has no permission for this session's child
def test_update_reading_session_without_permission(client, override_auth):
    override_auth("777")
    payload = {
        "book_id": "updated-book-id",
    }
    response = client.put(f"{SESSIONS_BASE_URL}/test-session-id-1", json=payload)
    assert response.status_code == 403
    assert response.json()["status"] == 403
    assert response.json()["error"] == "PERMISSION_DENIED"
    assert response.json()["message"] == "Insufficient permissions to complete this action"


# Negative Path: test 404 session not found
def test_update_reading_session_not_found(client, override_auth):
    override_auth("123")
    payload = {
        "book_id": "updated-book-id",
    }
    response = client.put(f"{SESSIONS_BASE_URL}/nonexistent-session-id", json=payload)
    assert response.status_code == 404
    assert response.json()["status"] == 404
    assert response.json()["error"] == "READING_SESSION_NOT_FOUND"
    assert response.json()["message"] == "Reading session with id: 'nonexistent-session-id' not found"


# Negative Path: test 401 unauthorised user - no auth override
def test_update_reading_session_as_unauthorised_user(client):
    response = client.put(f"{SESSIONS_BASE_URL}/test-session-id-1")
    assert response.status_code == 401
    assert response.json()["status"] == 401
    assert response.json()["error"] == "Not authenticated"
    assert response.json()["message"] == "Not authenticated"


# <--- COUNT READING SESSIONS TESTS --->

# Happy Path: test 200 success with count returned
def test_count_reading_sessions(client, override_auth):
    override_auth("123")
    response = client.get(f"{CHILDREN_BASE_URL}/test-child-id-2/reading-sessions/count")
    assert response.status_code == 200
    assert response.json() == 5


# Happy Path: test 200 success with zero count
def test_count_reading_sessions_zero(client, override_auth):
    override_auth("123")
    response = client.get(f"{CHILDREN_BASE_URL}/test-child-id-empty/reading-sessions/count")
    assert response.status_code == 200
    assert response.json() == 0


# Negative Path: test 403 user has no permission for this child
def test_count_reading_sessions_without_permission(client, override_auth):
    override_auth("777")
    response = client.get(f"{CHILDREN_BASE_URL}/test-child-id-2/reading-sessions/count")
    assert response.status_code == 403
    assert response.json()["status"] == 403
    assert response.json()["error"] == "PERMISSION_DENIED"
    assert response.json()["message"] == "Insufficient permissions to complete this action"


# Negative Path: test 401 unauthorised user - no auth override
def test_count_reading_sessions_as_unauthorised_user(client):
    response = client.get(f"{CHILDREN_BASE_URL}/test-child-id-2/reading-sessions/count")
    assert response.status_code == 401
    assert response.json()["status"] == 401
    assert response.json()["error"] == "Not authenticated"
    assert response.json()["message"] == "Not authenticated"
