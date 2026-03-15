"""
Tests the backend service across every layer

These tests are slower and more fragile than unit tests, and are intended to
provide confidence that the FastAPI endpoints continue to work while we refactor. 
Therefore, we're only including a basic set of happy path tests on each route.
Error handling is tested comprehensively via the unit testing at each layer.

A note about data:
    Assertions on specific data returns depend on seeded data being available
"""
from datetime import date

BASE_URL = "/api/children"


def test_post_create_child(client):
    dob = date(2025, 5, 2)
    payload = {
        "name": "Betty",
        "date_of_birth": dob.isoformat(),
        "avatar_url": None,
    }

    response = client.post(BASE_URL, json=payload)

    # Very light assertions, just sanity checks really
    assert response.status_code == 201
    assert response.json()["name"] == "Betty"

def test_get_children(client):
    response = client.get(BASE_URL)

    assert response.status_code == 200

    assert response.json()[0]["name"] == "Susie"

def test_get_child(client):
    # Debug: check what's in the db
    from sqlalchemy import select
    from tests.integration_tests.conftest import engine
    from app.persistence.sqlalchemy.tables import children
    with engine.connect() as conn:
        result = conn.execute(select(children)).fetchall()
        print("Children in db:", result)
    response = client.get(f'{BASE_URL}/abc123')

    assert response.status_code == 200
    assert response.json()["name"] == "Susie"

def test_put_update_child_name(client):
    payload = {
        "name": "Andy",
    }
    response = client.put(f'{BASE_URL}/abc123', json=payload)

    assert response.status_code == 200
    assert response.json()["name"] == "Andy"
