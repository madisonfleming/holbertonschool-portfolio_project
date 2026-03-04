import pytest
from app.services.facade import MLBFacade
from app.api.schemas.children import CreateChild
from app.domain.exceptions import UserNotFoundError, InvalidChildNameError

class FakeUser():
    def __init__(self, id: str):
        self.id = id

class FakeUserRepository():
    def get_by_firebase_uid(self, firebase_uid):
        if firebase_uid == "user-123":
            return FakeUser("user-123")
        if firebase_uid == "user-777":
            raise UserNotFoundError
        return None

# class FakeChild():
#     def __init__(self, name: str = "Susie", date_of_birth: str = "2023-12-05"):
#         self.created_at = "2026-02-18 04:39:42.220228"
#         self.updated_at = "2026-02-18 04:39:42.220228"
#         self.id = "123"
#         self.name = name
#         self.date_of_birth = date_of_birth
#         self.age = 2
#         self.avatar_url = "/avatars/mlb-avatar-robot.png"


class FakeChildRepository():
    def __init__(self):
        self.child = None

    def save(self, child):
        child.id = "child-123"
        self.child = child

    def get(self, child_id):
        if child_id == "child-123":
            return {
                "created_at": "2026-02-18 04:39:42.220228",
                "updated_at": "2026-02-18 04:39:42.220228",
                "id": "child-123",
                "name": "Susie",
                "date_of_birth": "2023-12-05",
                "age": 2,
                "avatar_url": "/avatars/mlb-avatar-robot.png"
            }
        if child_id == "child-456":
            return {
                "created_at": "2026-02-18 04:39:42.220228",
                "updated_at": "2026-02-18 04:39:42.220228",
                "id": "child-456",
                "name": "Bobby",
                "date_of_birth": "2024-11-23",
                "age": 1,
                "avatar_url": "/avatars/mlb-avatar-apple.png"
            }
        if child_id == "child-777":
            return

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
    
    def add_member(self, user_id, child_id, role):
        self.called_with = {
            "user_id": user_id,
            "child_id": child_id,
            "role": role,
        }

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
# Happy path
def test_create_child(facade):
    request = CreateChild(
        name="Betty",
        date_of_birth="2025-02-26",
        avatar_url=None
    )
    response = facade.create_child(
        request=request,
        firebase_uid="user-123"
    )
    # assert on the response
    assert response.name == "Betty"

    # assert that the call to child db was made
    assert facade.child_repository.child.name == "Betty"
    
    # assert that the call to relationship db was made
    assert facade.relationship_repository.called_with == {
        "user_id": "user-123",
        "child_id": "child-123",
        "role": "primary",
    }

# Error paths: wrong user, no child name in request
def test_wrong_user(facade):
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

def test_no_child_name(facade):
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