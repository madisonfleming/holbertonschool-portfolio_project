"""
These tests call the /users endpoint

Note that the facade layer is mocked via class FakeFacade:
 - does not test business logic or data persistence

FakeFacade methods and data are defined in conftest.py

"""

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

# Negative Path: test 401 user not found error
def test_get_nonexistent_user(client, override_auth):
    override_auth("777")
    response = client.get(BASE_URL)
    assert response.status_code == 401
    assert response.json()["status"] == 401
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
    assert response.status_code == 401
    assert response.json()["status"] == 401
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
