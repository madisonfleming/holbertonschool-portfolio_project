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

client = TestClient(app)

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