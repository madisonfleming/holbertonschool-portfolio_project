"""
Tests the backend service across every layer

These tests are slower and more fragile than unit tests, and are intended to
provide confidence that the FastAPI endpoints continue to work while we refactor. 
Therefore, we're only including a basic set of happy path tests on each route.
Error handling is tested comprehensively via the unit testing at each layer.

A note about data:
    Assertions on specific data returns depend on seeded data being available
"""

from fastapi.testclient import TestClient
from app.factory import create_app
from app.config import UnitTestingConfig
from app.api.auth_dependencies import auth_current_user
from app.api.dependencies import get_facade
import pytest


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

@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "testing")

@pytest.fixture
def reading_session_payload():
    return {
        "child_id": "123",
        "external_id": "book-ext-id",
        "source": "source",
        "title": "The Hungry Little Caterpillar",
        "author": "Eric Carle",
        "cover_url": "/cover",
        "logged_at": "2026-01-28",
    }

BASE_URL = "/api/reading-sessions"

@pytest.fixture
def created_reading_session(client, reading_session_payload):
    response = client.post(BASE_URL, json=reading_session_payload)
    return response.json()

def test_post_create_reading_session(client, reading_session_payload):
    response = client.post(BASE_URL, json=reading_session_payload)

    # Very light assertions, just sanity checks really
    assert response.status_code == 201
    assert response.json()["child_id"] == "123"

def test_get_reading_sessions(client, created_reading_session):
    # Act - get
    response = client.get("/api/children/123/reading-sessions")

    assert response.status_code == 200
    assert response.json()[0]["child_id"] == "123"


def test_put_update_session(client, created_reading_session):
    # Arrange - get reading session id
    session_id = created_reading_session["session_id"]
    
    # Update a field
    payload = {
        "logged_at": "2026-02-28T00:00:00",
    }

    # Act
    response = client.put(f'{BASE_URL}/{session_id}', json=payload)

    assert response.status_code == 200
    assert response.json()["logged_at"] == "2026-02-28T00:00:00"

def test_get_count_reading_sessions(client, created_reading_session):
    # Act
    response = client.get("/api/children/123/reading-sessions/count")

    assert response.status_code == 200
    assert response.json() == 1
