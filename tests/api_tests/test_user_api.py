"""
These tests call the /users endpoint

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
from app.domain.exceptions import UserNotFoundError
from app.services.exceptions import DuplicateUserError
import pytest

class FakeFacade:
    """ 
    Add facade mocks here 

    - Use dot notation in the return data to match pydantic models
    """
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
def app():
    app = create_app(UnitTestingConfig())
    app.dependency_overrides[get_facade] = lambda: FakeFacade()
    yield app
    app.dependency_overrides.clear()

@pytest.fixture
def client(app):
    return TestClient(app)

#Allow dynamic uid creation for auth dependency overrides
@pytest.fixture
def override_auth(app):
    def _override(uid: str):
        async def override():
            return {"uid" : uid}
        app.dependency_overrides[auth_current_user] = override
    return _override

# Set the env to "testing"
@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "testing")

BASE_URL = "/api/users/me"

# <--- GET USER TESTS --->
# Happy Path: test 200 success with data returned
def test_get_existing_user(client, override_auth):
    override_auth("123")
    response = client.get(BASE_URL)
    assert response.status_code == 200
    assert response.json()["id"] == "a686c824-25e6-4704-87a6-651938429111"
    assert response.json()["name"] == "Mary"
    assert response.json()["email"] == "mary@example.com"
    assert response.json()["role"] == "standard"

# Negative Path: test 404 user not found error
def test_get_nonexistent_user(client, override_auth):
    override_auth("777")
    response = client.get(BASE_URL)
    assert response.status_code == 404
    assert response.json()["status"] == 404
    assert response.json()["error"] == "USER_NOT_FOUND"
    assert response.json()["message"] == "User not found"

# Negative Path: test 401 unauthorised user - no auth override
def test_get_user_as_unauthorised_user(client):
    response = client.get(BASE_URL)
    assert response.status_code == 401
    assert response.json()["status"] == 401
    assert response.json()["error"] == "Not authenticated"
    assert response.json()["message"] == "Not authenticated"

# <--- UPDATE USER TESTS --->
# Happy Path: test 200 success update all fields of a user
def test_update_user(client, override_auth):
    override_auth("123")
    payload = {
        "name": "Mary-Anne",
        "email": "mary-anne@example.com"
    }
    response = client.put(BASE_URL, json=payload)
    assert response.status_code == 200
    assert response.json()["id"] == "a686c824-25e6-4704-87a6-651938429111"
    assert response.json()["name"] == "Mary-Anne"
    assert response.json()["email"] == "mary-anne@example.com"
    assert response.json()["role"] == "standard"

# Happy Path: test 200 success update only email of a user
def test_update_user_email(client, override_auth):
    override_auth("123")
    payload = {
        "email": "mary-anne@example.com"
    }
    response = client.put(BASE_URL, json=payload)
    assert response.status_code == 200
    assert response.json()["id"] == "a686c824-25e6-4704-87a6-651938429111"
    assert response.json()["name"] == "Mary"
    assert response.json()["email"] == "mary-anne@example.com"
    assert response.json()["role"] == "standard"

# Happy Path: test 200 success update only name of a user
def test_update_user_name(client, override_auth):
    override_auth("123")
    payload = {
        "name": "Mary-Anne"
    }
    response = client.put(BASE_URL, json=payload)
    assert response.status_code == 200
    assert response.json()["id"] == "a686c824-25e6-4704-87a6-651938429111"
    assert response.json()["name"] == "Mary-Anne"
    assert response.json()["email"] == "mary@example.com"
    assert response.json()["role"] == "standard"

# Negative Path: test 409 user attempts to update an email to another existing user's email 
def test_update_user_with_existing_email(client, override_auth):
    override_auth("123")
    payload = {
        "email": "john@example.com"
    }
    response = client.put(BASE_URL, json=payload)
    assert response.status_code == 409
    assert response.json()["status"] == 409
    assert response.json()["error"] == "USER_ALREADY_EXISTS"
    assert response.json()["message"] == "User already exists"

# Negative Path: test 404 user not found error
def test_update_nonexistent_user(client, override_auth):
    override_auth("777")
    payload = {
        "email": "johnny@example.com"
    }
    response = client.put(BASE_URL, json=payload)
    assert response.status_code == 404
    assert response.json()["status"] == 404
    assert response.json()["error"] == "USER_NOT_FOUND"
    assert response.json()["message"] == "User not found"

# Negative Path: test 401 unauthorised user - no auth override
def test_update_user_as_unauthorised_user(client):
    payload = {
        "email": "johnny@example.com"
    }
    response = client.put(BASE_URL, json=payload)
    assert response.status_code == 401
    assert response.json()["status"] == 401
    assert response.json()["error"] == "Not authenticated"
    assert response.json()["message"] == "Not authenticated"

# Negative Path: test 400 (invalid name format) raises custom RequestValidationError
def test_update_user_with_invalid_name(client, override_auth):
    override_auth("123")
    payload = {
        "name": 111
    }
    response = client.put(BASE_URL, json=payload)
    assert response.status_code == 400
    assert response.json()["error"] == "VALIDATION_ERROR"
    assert "('body', 'name')" in response.json()["message"]
    assert response.json()["status"] == 400

# Negative Path: test 400 (invalid email format) raises custom RequestValidationError
def test_update_user_with_invalid_email(client, override_auth):
    override_auth("123")
    payload = {
        "email": "fake-email"
    }
    response = client.put(BASE_URL, json=payload)
    assert response.status_code == 400
    assert response.json()["error"] == "VALIDATION_ERROR"
    assert "('body', 'email')" in response.json()["message"]
    assert response.json()["status"] == 400

# Negative path: attempt to update unexpected field #TODO: when request schema is restricted - update assertions in test 
def test_update_unknown_field(client, override_auth):
    override_auth("123")
    payload = {
        "pet": "dog"
    }
    response = client.put(BASE_URL, json=payload)
    assert response.status_code == 200
    assert response.json()["id"] == "a686c824-25e6-4704-87a6-651938429111"
    assert response.json()["name"] == "Mary"
    assert response.json()["email"] == "mary@example.com"
    assert response.json()["role"] == "standard"
