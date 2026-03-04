"""
Tests the backend service across every layer

These tests are slower and more fragile than unit tests, and are intended to
provide confidence that the FastAPI endpoints continue to work while we refactor. 
Therefore, we're only including a basic set of happy path tests on each route.
Error handling is tested comprehensively via the unit testing at each layer.
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

# <--- CREATE CHILD TESTS --->
# Happy Path: test 201 child created successfully
def test_create_child_profile(client):
    payload = {
        "name": "Betty",
        "date_of_birth": "2025-02-26",
        "avatar_url": None,
    }

    response = client.post(BASE_URL, json=payload)

    assert response.status_code == 201
    assert response.json()["name"] == "Betty"
    assert response.json()["avatar_url"] == None