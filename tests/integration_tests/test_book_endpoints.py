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

BASE_URL = "/api/books"

def test_get_books(client):
    response = client.get(f"{BASE_URL}/search?q=wild")
    assert response.status_code == 200
    assert response.json()[0]["title"] == "Where the Wild Things Are"

def test_get_book_by_id(client):
    book_id = "d5df0557-4d06-46c8-b4f3-105511e3000c"
    response = client.get(f"{BASE_URL}/{book_id}")
    assert response.status_code == 200
    assert response.json()["book_id"] == "d5df0557-4d06-46c8-b4f3-105511e3000c"
