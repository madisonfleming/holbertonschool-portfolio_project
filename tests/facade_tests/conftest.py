# Ensure test settings are applied first

import os
from app.config import get_settings

os.environ["ENVIRONMENT"] = "testing"
# os.environ["DATABASE_URL"] = "sqlite+pysqlite:///./test.db"
os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"
settings = get_settings()

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
            child = FakeChild("child-123", "Susie", "2023-12-05", "/avatars/mlb-avatar-robot.png")
            return child
        if child_id == "child-456":
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

    def update(self, child):
        child = FakeChild(
            id="child-123",
            name="Suzanne",
            date_of_birth="2025-03-07",
            avatar_url="/avatars/mlb-avatar-apple.png"
            )
        return child

class FakeReadingSessionRepository():
    pass

class FakeMilestoneRepository():
    pass

class FakeMilestoneCompletionRepository():
    pass

class FakeRelationshipRepository():
    def __init__(self):
        self.called_with = None
    
    def create_relationship(self, user_id, child_id, role, relationship_type):
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
    def get_relationship_type(self, user_id, child_id):
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
