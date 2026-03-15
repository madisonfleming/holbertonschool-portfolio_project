"""
Tests the backend service across every layer

These tests are slower and more fragile than unit tests, and are intended to
provide confidence that the FastAPI endpoints continue to work while we refactor. 
Therefore, we're only including a basic set of happy path tests on each route.
Error handling is tested comprehensively via the unit testing at each layer.

A note about data:
    Assertions on specific data returns depend on seeded data being available
"""
import pytest


@pytest.fixture
def reading_session_payload():
    return {
        "child_id": "abc123",
        "external_id": "/works/OAM123",
        "source": "openlibrary",
        "title": "Where the Wild Things Are",
        "author": "Maurice Sendak",
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
    assert response.json()["child_id"] == "abc123"

def test_get_reading_sessions(client, created_reading_session):
    # Act - get
    response = client.get("/api/children/abc123/reading-sessions")

    assert response.status_code == 200
    assert response.json()[0]["child_id"] == "abc123"


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
    response = client.get("/api/children/abc123/reading-sessions/count")

    assert response.status_code == 200
    assert response.json() == 1
