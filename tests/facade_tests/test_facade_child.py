import pytest
from app.services.facade import MLBFacade
from app.api.schemas.children import CreateChild, UpdateChild
from app.domain.exceptions import UserNotFoundError, InvalidChildNameError, ChildNotFoundError
from app.services.exceptions import InvalidRelationshipTypeError, RelationshipNotFoundError, PermissionDeniedError

class FakeUser():
    def __init__(self, id: str):
        self.id = id

class FakeUserRepository():
    def get_by_firebase_uid(self, firebase_uid):
        if firebase_uid == "user-123":
            return FakeUser("user-123")
        if firebase_uid == "user-456":
            return FakeUser("user-456")
        if firebase_uid == "user-789":
            return FakeUser("user-789")
        if firebase_uid == "user-111":
            return FakeUser("user-111")
        if firebase_uid == "user-777":
            raise UserNotFoundError
        
        return None

class FakeChild():
    def __init__(self, id, name, date_of_birth, avatar_url):
        self.id = id
        self.name = name
        self.date_of_birth = date_of_birth
        self.avatar_url = avatar_url
        self.age = 2

class FakeChildRepository():
    def __init__(self):
        self.child = None

    def save(self, child):
        child.id = "child-123"
        self.child = child

    def get(self, child_id):
        if child_id == "child-123":
            # return {
                # "created_at": "2026-02-18 04:39:42.220228",
                # "updated_at": "2026-02-18 04:39:42.220228",
                # "id": "child-123",
                # "name": "Susie",
                # "date_of_birth": "2023-12-05",
                # "age": 2,
                # "avatar_url": "/avatars/mlb-avatar-robot.png"
            # }
            child = FakeChild("child-123", "Susie", "2023-12-05", "/avatars/mlb-avatar-robot.png")
            return child
        if child_id == "child-456":
            # return {
            #     "created_at": "2026-02-18 04:39:42.220228",
            #     "updated_at": "2026-02-18 04:39:42.220228",
            #     "id": "child-456",
            #     "name": "Bobby",
            #     "date_of_birth": "2024-11-23",
            #     "age": 1,
            #     "avatar_url": "/avatars/mlb-avatar-apple.png"
            # }
            child = FakeChild("child-123", "Bobby", "2024-11-23", "/avatars/mlb-avatar-apple.png")
            return child
        if child_id == "child-777":
            return

    def get_by_ids(self, child_ids):
        result = []
        for child_id in child_ids:
            child = self.get(child_id)
            if child:
                result.append(child)
        return result


# To do:

    # def get_all(self):
    #     # Not needed on child_repository
    #     # - will be implemented on relationship_repository
    #     pass

    # def get_by_attribute(self, attr, value):
    #     return None

    # def update(self, id, data):
    #     pass

    # def delete(self, id):
    #     pass

    # def get_by_ids(self, child_ids):
        # child_ids: a list of child ids
        # returns: a list of child objects
        # result = []
        # for child_id in child_ids:
        #     child = self.get(child_id)
        #     if child:
        #         result.append(child)
        # return result

class FakeReadingSessionRepository():
    pass

class FakeMilestoneRepository():
    pass

class FakeMilestoneCompletionRepository():
    pass

class FakeRelationshipRepository():
    def __init__(self):
        self.called_with = None
    
    def add_member(self, user_id, child_id, role, relationship_type):
        self.called_with = {
            "user_id": user_id,
            "child_id": child_id,
            "role": role,
            "relationship_type": relationship_type,
        }

    def get_children_per_user(self, user_id):
        if user_id == "user-123":
            return [{
                "user_id": "user-123",
                "child_id": "child-123",
                # "relationship_type": "Parent", ## Purposefully removed to check compatibility with old seed data without this saved
                "role": "primary"
            }]
        if user_id == "user-456":
            return [{
                "user_id": "user-456",
                "child_id": "child-123",
                "relationship_type": "Parent",
                "role": "secondary"
            },
            {
                "user_id": "user-456",
                "child_id": "child-456",
                "relationship_type": "Parent",
                "role": "primary"
            }]
        if user_id == "user-111":
            return [{
                "user_id": "user-111",
                "child_id": "child-111",
                "relationship_type": "Mum",
                "role": "primary"
            }]
        return []
    def get_relationship(self, user_id, child_id):
        for rel in self.get_children_per_user(user_id):
            if rel["user_id"] == user_id and rel["child_id"] == child_id:
                return rel
        return None

    def has_role(
        self,
        user_id: str,
        child_id: str,
        role: str
    ):
        for relationship in self.get_children_per_user(user_id):
            if relationship["user_id"] == user_id and relationship["child_id"] == child_id:
                return relationship["role"] == role
        return False

class FakeBookRepository():
    pass

class FakeOpenLibraryAPI():
    pass

# create a facade
@pytest.fixture
def facade():
    facade = MLBFacade(
        user_repository=FakeUserRepository(),
        child_repository=FakeChildRepository(),
        reading_session_repository=FakeReadingSessionRepository(),
        milestone_repository=FakeMilestoneRepository(),
        milestone_completion_repository=FakeMilestoneCompletionRepository(),
        relationship_repository=FakeRelationshipRepository(),
        book_repository=FakeBookRepository(),
        open_library_api=FakeOpenLibraryAPI(),
    )
    yield facade

@pytest.fixture
def user(uid):
    return {"uid" : uid}

@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "testing")

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
    
    assert response.name == "Betty" # assert on the response
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
    assert response.name == "Betty" # assert on the response
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
    assert children[0].name == "Susie"

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
    assert children[0].relationship_type == "Parent"

# Happy path: role returned
def test_get_children_check_role_returned(facade):
    children = facade.get_children(
        firebase_uid="user-123"
    )
    assert children[0].role == "primary"


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
    assert child.name == "Susie"

# happy path: correct relationship type returned
def test_get_child_relationship_type(facade):
    child = facade.get_child(
        child_id="child-123",
        firebase_uid="user-123"
    )
    assert child.relationship_type == "Parent"

# happy path: correct role returned
def test_get_child_role(facade):
    child = facade.get_child(
        child_id="child-123",
        firebase_uid="user-123"
    )
    assert child.role == "primary"

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
    assert updated_child.name == "Suzanne"

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
    assert updated_child.name == "Susie"
    assert updated_child.age == 2


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
    assert updated_child.avatar_url == "/avatars/mlb-avatar-bee.png"

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
    assert updated_child.name == "Suzanne"
    assert updated_child.age == 2
    assert updated_child.avatar_url == "/avatars/mlb-avatar-bee.png"

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
    assert updated_child.name == "Susie"
    assert updated_child.age == 2
    assert updated_child.avatar_url == "/avatars/mlb-avatar-robot.png"

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
    assert updated_child.relationship_type == "Parent" # test default value "Parent" is returned when relationship type is not set in rel repo

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
    assert updated_child.role == "primary"

# Happy path: explicit check that the call to the child repo (save) was successful
def test_update_child_child_repo_called(facade):
    request = UpdateChild(
        name="Suzanne"
    )
    facade.update_child(
        child_id="child-123",
        request=request,
        firebase_uid="user-123"
    )
    assert facade.child_repository.child.name == "Suzanne" # assert the call to child repo was made
