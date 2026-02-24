"""
These tests calls the /children endpoint

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
        }

app = create_app(UnitTestingConfig())

app.dependency_overrides[get_facade] = lambda: FakeFacade()
app.dependency_overrides[auth_current_user] = lambda: {"uid" : "123"} # overrides the auth dependency

client = TestClient(app)

# <--- CREATE CHILD TESTS --->
# Happy Path: test 201 child created successfully
def test_create_child_profile():
    payload = {
        "name": "Betty",
        "date_of_birth": "2025-02-26",
        "avatar_url": None,
    }

    response = client.post("/children", json=payload)

    assert response.status_code == 201
    assert response.json()["name"] == "Betty"
    assert response.json()["age"] == 2
    assert response.json()["avatar_url"] == None

# Negative Path: test 400 (name missing) raises custom RequestValidationError
def test_create_child_with_missing_name():
    payload = {
        "date_of_birth": "2025-02-26",
        "avatar_url": None,
    }
    response = client.post("/children", json=payload)
    assert response.status_code == 400
    assert response.json()["error"] == "VALIDATION_ERROR"
    assert "('body', 'name')" in response.json()["message"]
    assert response.json()["status"] == 400

# Negative Path: test 400 (dob missing) raises custom RequestValidationError
def test_create_child_with_missing_dob():
    payload = {
        "name": "Betty",
        "avatar_url": None
    }
    response = client.post("/children", json=payload)
    assert response.status_code == 400
    assert response.json()["error"] == "VALIDATION_ERROR"
    assert "('body', 'date_of_birth')" in response.json()["message"]
    assert response.json()["status"] == 400

# Negative Path: test 400 (invalid DOB format) raises custom RequestValidationError
def test_create_child_with_invalid_field():
    payload = {
        "name": "Betty",
        "date_of_birth": "26-02-2025",
        "avatar_url": None,
    }
    response = client.post("/children", json=payload)
    assert response.status_code == 400
    assert response.json()["error"] == "VALIDATION_ERROR"
    assert "('body', 'date_of_birth')" in response.json()["message"]
    assert response.json()["status"] == 400

# Negative Path: test 401 unauthorised user
def test_create_child_401():
    # create a fresh app to use in this test only so auth dependency doesn't get overidden
    new_app = create_app(UnitTestingConfig())
    new_app.dependency_overrides[get_facade] = lambda: FakeFacade()
    new_client = TestClient(new_app)
    payload = {
        "name": "Betty",
        "date_of_birth": "2025-02-26",
        "avatar_url": None,
    }
    response = new_client.post("/children", json=payload)
    assert response.status_code == 401
    assert response.json()["status"] == 401
    assert response.json()["error"] == "Not authenticated"
    assert response.json()["message"] == "Not authenticated"
    
