import pytest
from app.services.facade import MLBFacade
from app.api.schemas.users import UpdateUser
from app.domain.exceptions import UserNotFoundError, InvalidChildNameError, ChildNotFoundError
from app.services.exceptions import InvalidRelationshipTypeError, RelationshipNotFoundError, PermissionDeniedError, DuplicateUserError

# <--- GET USER --->
# Error path: User not found
def test_get_user_wrong_user(facade):
    with pytest.raises(UserNotFoundError):
        facade.get_user(
            firebase_uid=None
    )

# Happy path: user found
def test_get_user_right_user(facade):
    user = facade.get_user(
        firebase_uid="user-789"
    )
    assert user.id == "user-789"
    

# <--- UPDATE USER --->
# Error path: user not found
def test_update_user_wrong_user(facade):
    request = UpdateUser(
        name="Annie"
    )
    with pytest.raises(UserNotFoundError):
        facade.update_user(
            request=request,
            firebase_uid=None
    )

# Happy path: name only updated
def test_update_user_name_only(facade):
    request = UpdateUser(
        name="Annie"
    )

    response = facade.update_user(
        request=request,
        firebase_uid="user-123"
    )
    assert response.name == "Annie"# assert on the response
    assert facade.user_repository.user.name == "Annie" # assert call to db made

# Happy path: email only updated
def test_update_user_email_only(facade):
    request = UpdateUser(
        email="annie@example.com"
    )
    response = facade.update_user(
        request=request,
        firebase_uid="user-123"
    )
    assert response.email == "annie@example.com" # assert on the response
    assert facade.user_repository.user.email == "annie@example.com" # assert call to db made

# Happy path: email + name updated
def test_update_user_name_and_email(facade):
    request = UpdateUser(
        name="Annie",
        email="annie@example.com"
    )
    response = facade.update_user(
        request=request,
        firebase_uid="user-123"
    )
    assert response.name == "Annie"# assert on the response
    assert response.email == "annie@example.com"
    assert facade.user_repository.user.name == "Annie" # assert call to db made
    assert facade.user_repository.user.email == "annie@example.com"

# Error path: email already exists with another user
def test_update_user_existing_email(facade):
    request = UpdateUser(
        email="betty@example.com"
    )
    with pytest.raises(DuplicateUserError):
        facade.update_user(
            request=request,
            firebase_uid="user-123"
    )
