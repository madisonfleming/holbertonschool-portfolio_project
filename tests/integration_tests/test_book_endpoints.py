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

BASE_URL = "/api/books"

# Commenting out until I figure out how to skip a call to the real OL endpoint
# def test_get_books(client):
#     response = client.get(f"{BASE_URL}/search?q=Where the Wild Things Are")
#     assert response.status_code == 200
#     assert response.json()[0]["title"] == "Where the Wild Things Are"

def test_get_book_by_id(client):
    book_id = "book123"
    response = client.get(f"{BASE_URL}/{book_id}")
    assert response.status_code == 200
    assert response.json()["book_id"] == "book123"