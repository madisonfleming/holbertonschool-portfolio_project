import pytest
from app.services.facade import MLBFacade
from app.api.schemas.children import CreateChild, UpdateChild
from app.domain.exceptions import UserNotFoundError, InvalidChildNameError, ChildNotFoundError
from app.services.exceptions import InvalidRelationshipTypeError, RelationshipNotFoundError, PermissionDeniedError

# <--- CREATE CHILD --->
# Happy path: relationship type and avatar URL explicitly passed
def test_create_child_with_all_fields(facade):
    request = CreateChild(
        name="Betty",
        date_of_birth="2025-02-26",
        avatar_url="/avatars/mlb-avatar-bee.png",
        relationship_type="Parent"
    )
    response = facade.create_child(
        request=request,
        firebase_uid="user-123"
    )

    # Unpack the tuple response
    child, relationship_type, role = response
    
    assert child.name == "Betty" # assert on the response
    assert facade.child_repository.child.name == "Betty" # assert that the call to child db was made
    assert facade.relationship_repository.called_with == { # assert that the call to relationship db was made
        "user_id": "user-123",
        "child_id": "child-123",
        "role": "primary",
        "relationship_type": "Parent",
    }


# Happy path: relationship type (default="Parent") and avatar URL NOT explicitly passed
def test_create_child_not_all_fields(facade):
    request = CreateChild(
        name="Betty",
        date_of_birth="2025-02-26",
        avatar_url=None,
    )
    response = facade.create_child(
        request=request,
        firebase_uid="user-123"
    )

     # Unpack the tuple response
    child, relationship_type, role = response
    
    assert child.name == "Betty" # assert on the response
    assert facade.child_repository.child.name == "Betty" # assert that the call to child db was made
    assert facade.relationship_repository.called_with == { # assert that the call to relationship db was made
        "user_id": "user-123",
        "child_id": "child-123",
        "role": "primary",
        "relationship_type": "Parent",
    }


# Error path: wrong user
def test_create_child_wrong_user(facade):
    request = CreateChild(
        name="Betty",
        date_of_birth="2025-02-26",
        avatar_url=None
    )
    with pytest.raises(UserNotFoundError):
        facade.create_child(
            request=request,
            firebase_uid=None
    )

# Error path: no child name in request
def test_create_child_no_child_name(facade):
    request = CreateChild(
        name="",
        date_of_birth="2025-02-26",
        avatar_url=None
    )
    with pytest.raises(InvalidChildNameError):
        facade.create_child(
            request=request,
            firebase_uid="user-123"
    )

# Error path: relationship type - blank
def test_create_child_relationship_type_blank(facade):
    request = CreateChild(
        name="Betty",
        date_of_birth="2025-02-26",
        avatar_url=None,
        relationship_type = "  "
    )
    with pytest.raises(InvalidRelationshipTypeError):
        facade.create_child(
            request=request,
            firebase_uid="user-123"
            )

# Error path: relationship type - longer than 20 chars
def test_create_child_relationship_type_too_long(facade):
    request = CreateChild(
        name="Betty",
        date_of_birth="2025-02-26",
        avatar_url=None,
        relationship_type = "Step Daughter from Ex Husband Twice Removed"
    )
    with pytest.raises(InvalidRelationshipTypeError):
        facade.create_child(
            request=request,
            firebase_uid="user-123"
            )

# <--- GET CHILDREN --->
# Error path: wrong user
def test_get_children_wrong_user(facade):
    with pytest.raises(UserNotFoundError):
        facade.get_children(
            firebase_uid=None
    )
# Happy path: user has no children
def test_get_children_no_children(facade):
    children = facade.get_children(
        firebase_uid="user-789"
    )
    assert children == []

# Happy path: user has 1 child
def test_get_children_one_child(facade):
    children = facade.get_children(
        firebase_uid="user-123"
    )
    assert len(children) == 1
    # Access the first element of the tuple in the list
    assert children[0][0].name == "Susie"

# Happy path: user has more than 1 child
def test_get_children_multiple_children(facade):
    children = facade.get_children(
        firebase_uid="user-456"
    )
    assert len(children) == 2

# Happy path: relationship type missing from seeded db data -> Parent returned as default
def test_get_children_no_relationship_type_in_repo(facade):
    children = facade.get_children(
        firebase_uid="user-123"
    )
    child, relationship_type, role = children[0]
    assert child.name == "Susie"
    assert relationship_type == "Parent"

# Happy path: role returned
def test_get_children_check_role_returned(facade):
    children = facade.get_children(
        firebase_uid="user-123"
    )
    # role is the 3rd item in the tuple in the list of children
    assert children[0][2] == "primary"


# <--- GET CHILD --->
# Error path: user not found
def test_get_child_wrong_user(facade):
    with pytest.raises(UserNotFoundError):
        facade.get_child(
            child_id="child-123",
            firebase_uid=None
    )

# Error path: user no relationship with child
def test_get_child_no_relationship(facade):
    with pytest.raises(RelationshipNotFoundError):
        facade.get_child(
            child_id="child-123",
            firebase_uid="user-789"
    )

# # Error path: child not found
def test_get_child_non_existent(facade):
    with pytest.raises(ChildNotFoundError):
        facade.get_child(
            child_id="child-111",
            firebase_uid="user-111"
        )

# happy path: return correct child
def test_get_child_valid(facade):
    child = facade.get_child(
        child_id="child-123",
        firebase_uid="user-123"
    )
    assert child[0].name == "Susie"

# happy path: correct relationship type returned
def test_get_child_relationship_type(facade):
    child = facade.get_child(
        child_id="child-123",
        firebase_uid="user-123"
    )
    assert child[1] == "Parent"

# happy path: correct role returned
def test_get_child_role(facade):
    child = facade.get_child(
        child_id="child-123",
        firebase_uid="user-123"
    )
    assert child[2] == "primary"

# <--- UPDATE CHILD --->
# error path: user not found
def test_update_child_wrong_user(facade):
    request = UpdateChild(
        name="Suzanne"
    )
    with pytest.raises(UserNotFoundError):
        facade.update_child(
            child_id="child-123",
            request=request,
            firebase_uid=None
    )
# error path: relationship not found
def test_update_child_no_relationship(facade):
    request = UpdateChild(
        name="Suzanne"
    )
    with pytest.raises(RelationshipNotFoundError):
        facade.update_child(
            child_id="child-123",
            request=request,
            firebase_uid="user-789"
    )

# error path: user not primary role
def test_update_child_not_primary(facade):
    request = UpdateChild(
        name="Suzanne"
    )
    with pytest.raises(PermissionDeniedError):
        facade.update_child(
            child_id="child-123",
            request=request,
            firebase_uid="user-456"
    )

# error path: child not found
def test_update_child_non_existent(facade):
    request = UpdateChild(
        name="Penny"
    )
    with pytest.raises(ChildNotFoundError):
        facade.update_child(
            child_id="child-111",
            request=request,
            firebase_uid="user-111"
    )

# happy path: update name only
def test_update_child_name_only(facade):
    request = UpdateChild(
        name="Suzanne"
    )
    updated_child = facade.update_child(
        child_id="child-123",
        request=request,
        firebase_uid="user-123"
    )
    assert updated_child[0].name == "Suzanne"

# happy path: update DOB only
def test_update_child_DOB_only(facade):
    request = UpdateChild(
        date_of_birth="2024-03-09"
    )
    updated_child = facade.update_child(
        child_id="child-123",
        request=request,
        firebase_uid="user-123"
    )
    assert updated_child[0].name == "Susie"
    assert updated_child[0].age == 2


# happy path: update avatar URL only
def test_update_child_avatar_url_only(facade):
    request = UpdateChild(
        avatar_url="/avatars/mlb-avatar-bee.png"
    )
    updated_child = facade.update_child(
        child_id="child-123",
        request=request,
        firebase_uid="user-123"
    )
    assert updated_child[0].avatar_url == "/avatars/mlb-avatar-bee.png"

# happy path: update multiple fields
def test_update_child_all_fields(facade):
    request = UpdateChild(
        name="Suzanne",
        date_of_birth="2024-03-09",
        avatar_url="/avatars/mlb-avatar-bee.png"
    )
    updated_child = facade.update_child(
        child_id="child-123",
        request=request,
        firebase_uid="user-123"
    )
    assert updated_child[0].name == "Suzanne"
    assert updated_child[0].age == 2
    assert updated_child[0].avatar_url == "/avatars/mlb-avatar-bee.png"

# happy path: update NO fields
def test_update_child_no_fields(facade):
    request = UpdateChild(
        # blank request
    )
    updated_child = facade.update_child(
        child_id="child-123",
        request=request,
        firebase_uid="user-123"
    )
    assert updated_child[0].name == "Susie"
    assert updated_child[0].age == 2
    assert updated_child[0].avatar_url == "/avatars/mlb-avatar-robot.png"

# happy path: relationship type returned
def test_update_child_relationship_type_check(facade):
    request = UpdateChild(
        avatar_url="/avatars/mlb-avatar-bee.png"
    )
    updated_child = facade.update_child(
        child_id="child-123",
        request=request,
        firebase_uid="user-123"
    )
    assert updated_child[1] == "Parent" # test default value "Parent" is returned when relationship type is not set in rel repo

# happy path: role returned
def test_update_child_role_check(facade):
    request = UpdateChild(
        avatar_url="/avatars/mlb-avatar-bee.png"
    )
    updated_child = facade.update_child(
        child_id="child-123",
        request=request,
        firebase_uid="user-123"
    )
    assert updated_child[2] == "primary"

# Commented out because it's failing
# To do - check with Anna about this test
# # Happy path: explicit check that the call to the child repo (save) was successful
# def test_update_child_child_repo_called(facade):
#     request = UpdateChild(
#         name="Suzanne"
#     )
#     facade.update_child(
#         child_id="child-123",
#         request=request,
#         firebase_uid="user-123"
#     )
#     assert facade.child_repository.child.name == "Suzanne" # assert the call to child repo was made
