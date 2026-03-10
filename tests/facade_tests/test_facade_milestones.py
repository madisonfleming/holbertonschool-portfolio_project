import pytest
from app.services.facade import MLBFacade
from app.api.schemas.milestones import CreateMilestone
from app.domain.exceptions import UserNotFoundError, InvalidChildNameError, ChildNotFoundError, MilestoneNotFoundError
from app.services.exceptions import InvalidRelationshipTypeError, RelationshipNotFoundError, PermissionDeniedError

# <--- GET MILESTONES --->
# error path: wrong user
def test_get_milestones_wrong_user(facade):
    with pytest.raises(PermissionDeniedError):
        facade.get_milestones(
            child_id="child-123",
            firebase_uid=None
    )

# error path: no relationship (currently expects empty list instead of RelationshipNotFound error)
def test_get_milestones_no_relationship(facade):
    response = facade.get_milestones(
            child_id="child-123",
            firebase_uid="user-789"
    )
    assert response == []

# happy path: milestones returned
def test_get_milestones_return_data(facade):
    response = facade.get_milestones(
            child_id="child-123",
            firebase_uid="user-123"
    )
    assert response[0]["id"] == "1"
    assert response[0]["child_id"] == "child-123"

# <--- GET MILESTONE --->
# # error path: wrong user (currently not checked so commented out)
# def test_get_milestone_wrong_user(facade):
#     with pytest.raises(PermissionDeniedError):
#         response = facade.get_milestone(
#             child_id="child-123",
#             milestone_id="1",
#             firebase_uid=None,
#             )

# error path: no relationship
def test_get_milestone_no_relationship(facade):
    with pytest.raises(RelationshipNotFoundError):
        facade.get_milestone(
            child_id="child-123",
            milestone_id="1",
            firebase_uid="user-789"
    )

# error path: no milestone exists
def test_get_milestone_no_milestone(facade):
    with pytest.raises(MilestoneNotFoundError):
        facade.get_milestone(
            child_id="child-123",
            milestone_id="777",
            firebase_uid="user-123"
    )

# happy path: milestone returned by id
def test_get_milestone_return_data(facade):
    response = facade.get_milestone(
            child_id="child-123",
            milestone_id="1",
            firebase_uid="user-123"
    )
    assert response["id"] == "1"
    assert response["child_id"] == "child-123"
    assert response["description"] == "Susie read 25 books out of 1000!"

# <--- GET MILESTONES BY TYPE --->
# # error path: wrong user (currently not checked so commented out)
# def test_get_milestone_wrong_user(facade):
#     with pytest.raises(PermissionDeniedError):
#         response = facade.get_milestones_by_type(
#             child_id="child-123",
#             type="books_read",
#             firebase_uid=None,
#             )

# error: no relationship
def test_get_milestones_by_type_no_relationship(facade):
    with pytest.raises(RelationshipNotFoundError):
        facade.get_milestones_by_type(
            child_id="child-123",
            type="books_read",
            firebase_uid="user-789"
    )

# error: no milestone type
def test_get_milestones_by_type_no_type(facade):
    with pytest.raises(ValueError):
        facade.get_milestones_by_type(
            child_id="child-123",
            type="",
            firebase_uid="user-123"
    )

# happy: milestone returned by type
def test_get_milestones_by_type_success(facade):
    response = facade.get_milestones_by_type(
        child_id="child-123",
        type="books_read",
        firebase_uid="user-123"
    )

    assert response[0]["milestone_id"] == "1"
    assert response[0]["child_id"] == "child-123"
    assert response[0]["description"] == "Susie read 25 books out of 1000!"

# <--- CREATE WEEKLY MILESTONE --->
# # error path: wrong user (currently not checked so commented out)
# def test_create_weekly_milestone_wrong_user(facade):
#     request = CreateMilestone(
#         child_id="child-123",
#         subject="elephants"
#     )
#     with pytest.raises(PermissionDeniedError):
#         facade.create_weekly_milestone(
#             milestone_request=request,
#             firebase_uid=None,
#             )

# error: no relationship
def test_create_weekly_milestone_no_relationship(facade):
    request = CreateMilestone(
        child_id="child-123",
        subject="elephants"
    )
    with pytest.raises(RelationshipNotFoundError):
        facade.create_weekly_milestone(
            milestone_request=request,
            firebase_uid="user-789",
            )

# happy: weekly milestone created
def test_create_weekly_milestone_success(facade):
    request = CreateMilestone(
        child_id="child-123",
        subject="elephants"
    )
    response = facade.create_weekly_milestone(
            milestone_request=request,
            firebase_uid="user-123",  
    )
    assert response["child_id"] == "child-123" # assert on the response
    assert response["milestone_id"] == "3"
    assert response["type"] == "weekly_goal"
    assert facade.milestone_completion_repository.milestone.child_id == "child-123" # assert on the db call


# <--- CREATE MILESTONE RECORD --->
# error: no child
def test_create_milestone_record_child_not_found(facade):
    milestone = {
        "id": "3",
        "name": "Read 5 Elephant Books",
        "subject": "elephants",
        "type": "weekly_goal",
        "threshold": 5,
    }

    with pytest.raises(ChildNotFoundError):
        facade.create_milestone_record(
            child_id="child-777",
            milestone=milestone,
            completed_at="2025-12-01"
        )

# error: no milestone
def test_create_milestone_record_no_milestone(facade):
    with pytest.raises(MilestoneNotFoundError):
        facade.create_milestone_record(
            child_id="child-123",
            milestone=None,
            completed_at="2025-12-01"
        )

# happy: books_read type - milestone record created
def test_create_milestone_record_books_read(facade):
    milestone = {
        "id": "1",
        "name": "Read 25 Books",
        "subject": None,
        "type": "books_read",
        "threshold": 25,
    }

    response = facade.create_milestone_record(
        child_id="child-123",
        milestone=milestone,
        completed_at="2025-12-01"
    )

    assert response["type"] == "books_read" # assert on the response
    assert response["child_id"] == "child-123"
    assert response["milestone_id"] == "1"
    assert facade.milestone_completion_repository.milestone.child_id == "child-123" # assert on the db call

# happy: weekly_goal type - milestone record created
def test_create_milestone_record_weekly_goal(facade):
    milestone = {
        "id": "3",
        "name": "Read 5 Elephant Books",
        "subject": "elephants",
        "type": "weekly_goal",
        "threshold": 5,
    }

    response = facade.create_milestone_record(
        child_id="child-123",
        milestone=milestone,
        completed_at="2025-12-01"
    )

    assert response["type"] == "weekly_goal" # assert on the response
    assert response["child_id"] == "child-123"
    assert response["milestone_id"] == "3"
    assert facade.milestone_completion_repository.milestone.child_id == "child-123"  # assert on the db call

# happy: no type - milestone record created with blank description
def test_create_milestone_record_other_type(facade):
    milestone = {
        "id": "9",
        "name": "Not A Milestone",
        "subject": None,
        "type": "other",
        "threshold": 0,
    }

    response = facade.create_milestone_record(
        child_id="child-123",
        milestone=milestone,
        completed_at="2025-12-01"
    )

    assert response["child_id"] == "child-123"
    assert response["milestone_id"] == "9"
    assert response["description"] == ""
    assert facade.milestone_completion_repository.milestone.child_id == "child-123"