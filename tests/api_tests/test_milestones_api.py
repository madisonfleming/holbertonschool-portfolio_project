"""
These tests call the /milestones endpoints

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

BASE_URL = "/api/children/child-123/milestones"
# BASE_URL = "/api/children/child-123/milestones"


# <--- GET ALL MILESTONES --->

# Happy Path: test 200 get all milestones
def test_get_all_milestones(client, override_auth):
    override_auth("123")

    response = client.get(f'{BASE_URL}')
    assert response.status_code == 200
    assert response.json()[0]["id"] == "milestone-123"
    assert response.json()[0]["child_id"] == "child-123"
    assert response.json()[1]["id"] == "milestone-124"
    assert response.json()[1]["child_id"] == "child-123"
    assert response.json()[0]["metric_key"] != response.json()[1]["metric_key"]

# Happy Path: test 200 get all milestones by metric key
def test_get_all_milestones_by_metric_key(client, override_auth):
    override_auth("123")

    response = client.get(f'{BASE_URL}', params={"metric_key": "weekly_goal"})
    assert response.status_code == 200
    assert response.json()[0]["id"] == "milestone-121"
    assert response.json()[0]["child_id"] == "child-123"

# Negative path: test user<>child relationship not found returns empty list
def test_get_all_milestones_without_userchild_relationship(client, override_auth):
    override_auth("777")

    response = client.get(f'{BASE_URL}')
    assert response.status_code == 200
    assert response.json() == []

# Negative path: test unauthorised access
def test_get_all_milestones_with_unauthorised_user(client):

    response = client.get(f'{BASE_URL}')
    assert response.status_code == 401

# <--- GET ONE MILESTONE --->

# Happy Path: test 200 get one milestone
def test_get_one_milestone(client, override_auth):
    override_auth("123")

    response = client.get(f'{BASE_URL}/milestone-123')
    assert response.status_code == 200
    assert response.json()["id"] == "milestone-123"
    assert response.json()["child_id"] == "child-123"

# # Happy Path: test 200 get all milestones by metric key
# def test_get_all_milestones_by_metric_key(client, override_auth):
#     override_auth("123")

#     response = client.get(f'{BASE_URL}', params={"metric_key": "weekly_goal"})
#     assert response.status_code == 200
#     assert response.json()[0]["id"] == "milestone-122"
#     assert response.json()[0]["child_id"] == "child-123"

# # Negative path: test user<>child relationship not found
# def test_get_all_milestones_without_userchild_relationship(client, override_auth):
#     override_auth("777")

#     response = client.get(f'{BASE_URL}')
#     assert response.status_code == 403

# # Negative path: test unauthorised access
# def test_get_all_milestones_with_unauthorised_user(client):

#     response = client.get(f'{BASE_URL}')
#     assert response.status_code == 401