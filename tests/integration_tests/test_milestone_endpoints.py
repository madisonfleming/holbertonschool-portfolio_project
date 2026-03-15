"""
Tests the backend service across every layer

These tests are slower and more fragile than unit tests, and are intended to
provide confidence that the FastAPI endpoints continue to work while we refactor. 
Therefore, we're only including a basic set of happy path tests on each route.
Error handling is tested comprehensively via the unit testing at each layer.

A note about data:
    Assertions on specific data returns depend on seeded data being available
"""

BASE_URL = "/api/children/abc123/milestones" #child id is susie

def test_get_all_milestones(client):
    response = client.get(BASE_URL)

    assert response.status_code == 200
    assert response.json()[0]["id"] == "ms-completion-123"

def test_get_one_milestone(client):
    milestone_id = "ms-completion-123"
    response = client.get(f"{BASE_URL}/{milestone_id}")

    assert response.status_code == 200
    assert response.json()["child_id"] == "abc123"
    assert response.json()["id"] == "ms-completion-123"

def test_post_weekly_milestone(client):
    payload = {
        "child_id": "abc123",
        "subject": "elephants"
    }
    response = client.post(BASE_URL, json=payload)

    assert response.status_code == 201
    assert response.json()["child_id"] == "abc123"
