"""
Tests the backend service across every layer

These tests are slower and more fragile than unit tests, and are intended to
provide confidence that the FastAPI endpoints continue to work while we refactor. 
Therefore, we're only including a basic set of happy path tests on each route.
Error handling is tested comprehensively via the unit testing at each layer.

A note about data:
    Assertions on specific data returns depend on seeded data being available
"""
    

BASE_URL = "/api/users/me"


def test_get_user(client):
    response = client.get(BASE_URL)

    assert response.status_code == 200

    assert response.json()["name"] == "Alice"


def test_put_update_user_name(client):
    payload = {
        "name": "Andy",
    }
    response = client.put(BASE_URL, json=payload)

    assert response.status_code == 200
    assert response.json()["name"] == "Andy"
