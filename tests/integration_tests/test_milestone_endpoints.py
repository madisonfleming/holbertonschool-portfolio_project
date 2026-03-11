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

BASE_URL = "/api/children/e686c824-25e6-4704-87a6-651938429111/milestones" #child id is susie

def test_get_all_milestones(client):
    response = client.get(BASE_URL)

    assert response.status_code == 200
    assert response.json()[0]["id"] == "2"

def test_get_one_milestone(client):
    milestone_id = "1"
    response = client.get(f"{BASE_URL}/{milestone_id}")

    assert response.status_code == 200
    assert response.json()["child_id"] == "e686c824-25e6-4704-87a6-651938429111"
    assert response.json()["id"] == "1"

def test_post_weekly_milestone(client):
    payload = {
        "child_id": "e686c824-25e6-4704-87a6-651938429111",
        "subject": "elephants"
    }
    response = client.post(BASE_URL, json=payload)

    assert response.status_code == 201
    assert response.json()["child_id"] == "e686c824-25e6-4704-87a6-651938429111"
