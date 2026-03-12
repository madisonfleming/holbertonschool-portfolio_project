"""
These tests calls the /children endpoint

Validates that each method on the endpoint:
  - accepts a valid request payload
  - validates the payload using a Pydantic input model
  - calls the facade layer, delegating business logic to the facade
  - returns a response that matches the expected Pydantic response 
    schema

Note that the facade layer is mocked via class FakeFacade:
 - does not test business logic or data persistence

FakeFacade methods and data are defined in conftest.py
"""


BASE_URL = "/api/children"

# <--- CREATE CHILD TESTS --->
# Happy Path: test 201 child created successfully (user specifies relationship)
# Qu: is the new tuple at risk of divergence between the domain model and the direct role/relationship return?
def test_create_child_profile_with_relationship(client, override_auth):
    override_auth("123")
    payload = {
        "name": "Betty",
        "date_of_birth": "2025-02-26",
        "avatar_url": None,
        "relationship_type": "Sister"
    }

    response = client.post(BASE_URL, json=payload)
    assert response.status_code == 201
    assert response.json()["name"] == "Betty"
    assert response.json()["age"] == 2
    assert response.json()["avatar_url"] == None
    assert response.json()["relationship_type"] == "Sister"
    assert response.json()["role"] == "primary"

# Happy Path: test 201 child created successfully (user doesn't specify relationship)
def test_create_child_profile_without_relationship(client, override_auth):
    override_auth("123")
    payload = {
        "name": "Betty",
        "date_of_birth": "2025-02-26",
        "avatar_url": None,
        "relationship_type": None
    }

    response = client.post(BASE_URL, json=payload)
    assert response.status_code == 201
    assert response.json()["name"] == "Betty"
    assert response.json()["age"] == 2
    assert response.json()["avatar_url"] == None
    assert response.json()["relationship_type"] == "Parent" # gets defaults value
    assert response.json()["role"] == "primary"

# Negative Path: test 400 (name missing) raises custom RequestValidationError
def test_create_child_with_missing_name(client, override_auth):
    override_auth("123")
    payload = {
        "date_of_birth": "2025-02-26",
        "avatar_url": None,
    }
    response = client.post(BASE_URL, json=payload)
    assert response.status_code == 400
    assert response.json()["error"] == "VALIDATION_ERROR"
    assert "('body', 'name')" in response.json()["message"]
    assert response.json()["status"] == 400

# Negative Path: test 400 (dob missing) raises custom RequestValidationError
def test_create_child_with_missing_dob(client, override_auth):
    override_auth("123")
    payload = {
        "name": "Betty",
        "avatar_url": None
    }
    response = client.post(BASE_URL, json=payload)
    assert response.status_code == 400
    assert response.json()["error"] == "VALIDATION_ERROR"
    assert "('body', 'date_of_birth')" in response.json()["message"]
    assert response.json()["status"] == 400

# Negative Path: test 400 (invalid DOB format) raises custom RequestValidationError
def test_create_child_with_invalid_dob(client, override_auth):
    override_auth("123")
    payload = {
        "name": "Betty",
        "date_of_birth": "26-02-2025",
        "avatar_url": None,
    }
    response = client.post(BASE_URL, json=payload)
    assert response.status_code == 400
    assert response.json()["error"] == "VALIDATION_ERROR"
    assert "('body', 'date_of_birth')" in response.json()["message"]
    assert response.json()["status"] == 400

# Negative Path: test 401 unauthorised user - no auth override
def test_create_child_as_unauthorised_user(client):
    payload = {
        "name": "Betty",
        "date_of_birth": "2025-02-26",
        "avatar_url": None,
    }
    response = client.post(BASE_URL, json=payload)
    assert response.status_code == 401
    assert response.json()["status"] == 401
    assert response.json()["error"] == "Not authenticated"
    assert response.json()["message"] == "Not authenticated"


# <--- GET CHILDREN TESTS --->
# Happy Path: test 200 success with data returned
def test_get_children_with_data(client, override_auth):
    override_auth("123")
    response = client.get(BASE_URL)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    assert response.json()[0]["id"] == "test-child-id-2"
    assert response.json()[0]["name"] == "Susie"
    assert response.json()[0]["age"] == 2
    assert response.json()[0]["avatar_url"] == None
    assert response.json()[0]["relationship_type"] == "Parent"
    assert response.json()[0]["role"] == "primary"

    assert response.json()[1]["id"] == "test-child-id-3"
    assert response.json()[1]["name"] == "Billy"
    assert response.json()[1]["age"] == 1
    assert response.json()[1]["avatar_url"] == None
    assert response.json()[1]["relationship_type"] == "Parent"
    assert response.json()[1]["role"] == "primary"

# Happy Path: test 200 success without data returned
def test_get_children_without_data(client, override_auth):
    override_auth("777")
    response = client.get(BASE_URL)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json() == []

# Negative Path: test 401 unauthorised user - no auth override
def test_get_children_as_unauthorised_user(client):
    response = client.get(BASE_URL)
    assert response.status_code == 401
    assert response.json()["status"] == 401
    assert response.json()["error"] == "Not authenticated"
    assert response.json()["message"] == "Not authenticated"

# <--- GET CHILD TESTS --->
# Happy Path: test 200 success with child returned
def test_get_child(client, override_auth):
    override_auth("123")

    response = client.get(f'{BASE_URL}/test-child-id-2')
    assert response.status_code == 200
    assert response.json()["id"] == "test-child-id-2"
    assert response.json()["name"] == "Susie"
    assert response.json()["age"] == 2
    assert response.json()["avatar_url"] == None
    assert response.json()["relationship_type"] == "Parent"
    assert response.json()["role"] == "primary"

# Negative Path: test 404 relationship between user and child id not found
def test_get_child_without_relo(client, override_auth):
    override_auth("777")
    response = client.get(f'{BASE_URL}/test-child-id-2')
    assert response.status_code == 403
    assert response.json()["status"] == 403
    assert response.json()["error"] == "RELATIONSHIP_NOT_FOUND"
    assert response.json()["message"] == "Relationship between user: '777' and child: 'test-child-id-2' not found"

# Negative Path: test 401 unauthorised user - no auth override
def test_get_child_as_unauthorised_user(client):
    response = client.get(f'{BASE_URL}/test-child-id-2')
    assert response.status_code == 401
    assert response.json()["status"] == 401
    assert response.json()["error"] == "Not authenticated"
    assert response.json()["message"] == "Not authenticated"

# <--- UPDATE CHILD TESTS --->
# Happy Path: test 200 success update all fields of a child (user 123)
def test_update_child(client, override_auth):
    override_auth("123")
    payload = {
    "name": "Suzanne",
    "date_of_birth": "2023-02-24",
    "avatar_url": "alien_avatar.com"
    }
    response = client.put(f'{BASE_URL}/test-child-id-2', json=payload)
    assert response.status_code == 200
    assert response.json()["id"] == "test-child-id-2"
    assert response.json()["name"] == "Suzanne"
    assert response.json()["age"] == 2
    assert response.json()["avatar_url"] == "alien_avatar.com"
    assert response.json()["relationship_type"] == "Parent"
    assert response.json()["role"] == "primary"

# Negative Path: test 400 (invalid DOB format) raises custom RequestValidationError (user 123)
def test_update_child_with_invalid_dob(client, override_auth):
    override_auth("123")
    payload = {
        "date_of_birth": "26-02-2025"
    }
    response = client.put(f'{BASE_URL}/test-child-id-2', json=payload)
    assert response.status_code == 400
    assert response.json()["error"] == "VALIDATION_ERROR"
    assert "('body', 'date_of_birth')" in response.json()["message"]
    assert response.json()["status"] == 400

# Negative Path: test 404 relationship between user and child id not found (user 777)
def test_update_child_without_relo(client, override_auth):
    override_auth("777")
    payload = {
    "name": "Suzanne",
    "date_of_birth": "2023-02-24",
    "avatar_url": "alien_avatar.com"
    }
    response = client.put(f'{BASE_URL}/test-child-id-2', json=payload)
    assert response.status_code == 403
    assert response.json()["status"] == 403
    assert response.json()["error"] == "RELATIONSHIP_NOT_FOUND"
    assert response.json()["message"] == "Relationship between user: '777' and child: 'test-child-id-2' not found"

# Negative Path: test 401 unauthorised user - no auth override
def test_update_child_as_unauthorised_user(client):
    response = client.put(f'{BASE_URL}/test-child-id-2')
    assert response.status_code == 401
    assert response.json()["status"] == 401
    assert response.json()["error"] == "Not authenticated"
    assert response.json()["message"] == "Not authenticated"
