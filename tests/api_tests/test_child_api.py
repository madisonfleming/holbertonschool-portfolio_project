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
    def get_children(self, firebase_uid):
        if firebase_uid == "123":
            return [
                {
                    "id": "e686c824-25e6-4704-87a6-651938429111",
                    "name": "Susie",
                    "age": 2,
                    "avatar_url": None,
                },
                {
                    "id": "e686c824-25e6-4704-87a6-651938429112",
                    "name": "Billy",
                    "age": 1,
                    "avatar_url": None,
                }]
        if firebase_uid == "777":
            return []



# app without auth dependency override (used only for 401 user unauthorised tests)
app_no_auth = create_app(UnitTestingConfig())
app_no_auth.dependency_overrides[get_facade] = lambda: FakeFacade()
client_no_auth = TestClient(app_no_auth)

# app with auth dependency overridden & fb uid of "123" (used for all other tests except 401)
# user 123 mocks an authorised user with kids
app_auth = create_app(UnitTestingConfig())
app_auth.dependency_overrides[get_facade] = lambda: FakeFacade()
app_auth.dependency_overrides[auth_current_user] = lambda: {"uid" : "123"} # overrides the auth dependency at endpoint and sets fbuid to "123"
client_auth = TestClient(app_auth)

# temp app with auth dependency overridden & fb uid of "777" (used for all other tests except 401)
# user 777 mocks an authorised user with no kids
temp_app = create_app(UnitTestingConfig())
temp_app.dependency_overrides[get_facade] = lambda: FakeFacade()
temp_app.dependency_overrides[auth_current_user] = lambda: {"uid" : "777"} # overrides the auth dependency at endpoint and sets fbuid to "777"
temp_client = TestClient(temp_app)

# <--- CREATE CHILD TESTS --->
# Happy Path: test 201 child created successfully
def test_create_child_profile():
    payload = {
        "name": "Betty",
        "date_of_birth": "2025-02-26",
        "avatar_url": None,
    }

    response = client_auth.post("/children", json=payload)

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
    response = client_auth.post("/children", json=payload)
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
    response = client_auth.post("/children", json=payload)
    assert response.status_code == 400
    assert response.json()["error"] == "VALIDATION_ERROR"
    assert "('body', 'date_of_birth')" in response.json()["message"]
    assert response.json()["status"] == 400

# Negative Path: test 400 (invalid DOB format) raises custom RequestValidationError
def test_create_child_with_invalid_dob():
    payload = {
        "name": "Betty",
        "date_of_birth": "26-02-2025",
        "avatar_url": None,
    }
    response = client_auth.post("/children", json=payload)
    assert response.status_code == 400
    assert response.json()["error"] == "VALIDATION_ERROR"
    assert "('body', 'date_of_birth')" in response.json()["message"]
    assert response.json()["status"] == 400

# Negative Path: test 401 unauthorised user
def test_create_child_as_unauthorised_user():
    payload = {
        "name": "Betty",
        "date_of_birth": "2025-02-26",
        "avatar_url": None,
    }
    response = client_no_auth.post("/children", json=payload)
    assert response.status_code == 401
    assert response.json()["status"] == 401
    assert response.json()["error"] == "Not authenticated"
    assert response.json()["message"] == "Not authenticated"
    
# <--- GET CHILDREN TESTS --->
# Happy Path: test 200 success with data returned
def test_get_children_with_data():
    response = client_auth.get("/children")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]["name"] == "Susie"
    assert response.json()[1]["name"] == "Billy"

# Happy Path: test 200 success without data returned
def test_get_children_without_data():
    response = temp_client.get("/children")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json() == []

# Negative Path: test 401 unauthorised user
def test_get_children_as_unauthorised_user():
    response = client_no_auth.get("/children")
    assert response.status_code == 401
    assert response.json()["status"] == 401
    assert response.json()["error"] == "Not authenticated"
    assert response.json()["message"] == "Not authenticated"

