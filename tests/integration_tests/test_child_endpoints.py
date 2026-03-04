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
import pytest


@pytest.fixture
def app():
    app = create_app(UnitTestingConfig())
    app.dependency_overrides[auth_current_user] = lambda uid = "123": {"uid": uid }
    yield app
    app.dependency_overrides.clear()

@pytest.fixture
def client(app):
    return TestClient(app)

# Set the env to "testing"
@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "testing")

BASE_URL = "/api/children"


def test_post_create_child(client):
    payload = {
        "name": "Betty",
        "date_of_birth": "2025-02-26",
        "avatar_url": None,
    }

    response = client.post(BASE_URL, json=payload)

    # Very light assertions, just sanity checks really
    assert response.status_code == 201
    assert response.json()["name"] == "Betty"

def test_get_children(client):
    response = client.get(BASE_URL)

    assert response.status_code == 200

    assert response.json()[0]["name"] == "Susie"

def test_get_child(client):
    response = client.get(f'{BASE_URL}/123')

    assert response.status_code == 200
    assert response.json()["name"] == "Amy"

def test_put_update_child_name(client):
    payload = {
        "name": "Andy",
    }
    response = client.put(f'{BASE_URL}/123', json=payload)

    assert response.status_code == 200
    assert response.json()["name"] == "Andy"
