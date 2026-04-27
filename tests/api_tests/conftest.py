"""
This file defines a FakeFacade class and the fixtures shared by the API test files
"""
# Ensure test settings are applied first

import os
from app.config import get_settings

os.environ["ENVIRONMENT"] = "testing"
os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"
settings = get_settings()

import pytest
from fastapi.testclient import TestClient
from app.factory import create_app
from app.config import UnitTestingConfig
from app.api.dependencies import get_facade
from app.api.auth_dependencies import auth_current_user
from app.services.exceptions import RelationshipNotFoundError, PermissionDeniedError, ReadingSessionNotFoundError, DuplicateUserError
from app.domain.exceptions import UserNotFoundError
from app.api.schemas.milestones import MilestoneCompletionResponse
from app.api.schemas.children import ChildResponse
from app.api.schemas.users import UserResponse
from app.domain.reading_sessions import ReadingSession
from datetime import datetime, timezone

class FakeFacade:
    """ 
    Add facade mocks here 

    - Use dot notation in the return data to match pydantic models
    """


    def create_child(self, child_data, firebase_uid="123"):
        relationship_type = child_data.relationship_type or "Parent"
        child = self.create_child_data(
            name="Betty",
            relationship_type=relationship_type,
            role="primary"
        )
        return child, relationship_type, "primary"
        # return child, relationship_type, "primary"
    
    def get_children(self, firebase_uid):
        if firebase_uid == "123":
            child1 = (self.create_child_data(
                    id="test-child-id-2",
                    name="Susie",
                    age=2,
                    avatar_url=None,
                    relationship_type="Parent",
                    role="primary"
                ), "Parent", "primary")
            child2 = (self.create_child_data(
                    id="test-child-id-3",
                    name="Billy",
                    age=1,
                    avatar_url=None,
                    relationship_type="Parent",
                    role="primary"
                ), "Parent", "primary")

            return [child1, child2]
        if firebase_uid == "777":
            return []

    def get_child(self, child_id, firebase_uid):
        if firebase_uid == "123" and child_id == "test-child-id-2":
            child = (self.create_child_data(id="test-child-id-2"))
            return (child, "Parent", "primary")
        if firebase_uid == "777":
            raise RelationshipNotFoundError("777", "test-child-id-2") # this should catch before ChildNotFoundError() in real facade

    def update_child(self, child_id, child_data, firebase_uid):
        if firebase_uid == "123" and child_id == "test-child-id-2":
            child = self.create_child_data(id=child_id, name=child_data.name, avatar_url=child_data.avatar_url)
            return (child, "Parent", "primary")

        if firebase_uid == "777":
            raise RelationshipNotFoundError("777", "test-child-id-2")
    
    # Helper method
    def create_child_data(
            self,
            id: str = "test-child-id",
            name: str = "Susie",
            age: int = 2,
            avatar_url: str | None = None,
            relationship_type: str = "Parent",
            role: str = "primary",
            ):
        print("relationship type: ", relationship_type)
        return ChildResponse(
            id=id,
            name=name,
            age=age,
            avatar_url=avatar_url,
            relationship_type=relationship_type or "Parent",
            role=role
        )
    
    def create_reading_session(self, reading_session_data, firebase_uid):
        return self.create_reading_session_data(
            session_id="test-session-id",
            child_id=reading_session_data.child_id,
        )

    def get_reading_sessions(self, child_id, firebase_uid, limit=None, from_date=None, to_date=None):
        if firebase_uid == "123" and child_id == "test-child-id-2":
            return [
                self.create_reading_session_data(child_id=child_id),
                self.create_reading_session_data(session_id="test-session-id-2", child_id=child_id, book_id="test-book-id-2"),
            ]
        
        if firebase_uid == "777":
            raise PermissionDeniedError()  # "Insufficient permissions to complete this action"
        if firebase_uid == "123" and child_id == "test-child-id-empty":
            return []
    
    
    def update_session(self, session_id, updated_session_data, firebase_uid):
        if firebase_uid == "123" and session_id == "test-session-id-1":
            # create object
            session = self.create_reading_session_data()
            # update attributes
            session.external_id = updated_session_data.external_id
            session.title = updated_session_data.title
            session.author = updated_session_data.author

            return session

        if firebase_uid == "777":
            raise PermissionDeniedError()  # "Insufficient permissions to complete this action"
        if session_id == "nonexistent-session-id":
            raise ReadingSessionNotFoundError(session_id)  # "Reading session with id: 'nonexistent-session-id' not found"

    def count_reading_sessions(self, child_id, firebase_uid, from_date=None, to_date=None):
        if firebase_uid == "123" and child_id == "test-child-id-2":
            return 5
        if firebase_uid == "123" and child_id == "test-child-id-empty":
            return 0
        if firebase_uid == "777":
            raise PermissionDeniedError()  # "Insufficient permissions to complete this action"

    # Helper method
    def create_reading_session_data(
            self,
            session_id: str = "test-session-id-1",
            child_id: str = "test-child-id-1",
            book_id: str = "test-book-id-1",
            ):
        timestamp = datetime.now(timezone.utc)

        reading_session = ReadingSession(
            id=session_id,
            child_id=child_id,
            external_id="external-id-1",
            book_id=book_id,
            title="My Little Pony",
            cover_url="/cover",
            logged_at=timestamp,
            created_at=timestamp,
            updated_at=timestamp,         
        )

        # reading_session = ReadingSessionResponse(
        #     session_id=session_id,
        #     child_id=child_id,
        #     book_id=book_id,
        #     title="My Little Pony",
        #     cover_url="/cover",
        #     logged_at=timestamp
        # )

        return reading_session
    
    def get_user(self, firebase_uid):
        if firebase_uid == "123":
            return self.create_user_data()
        else:
            raise UserNotFoundError()

    def update_user(self, request, firebase_uid):
        if firebase_uid == "123" and request.email != "john@example.com":
            name = request.name or "Mary"
            email = request.email or "mary@example.com"
            user = self.create_user_data(name, email)
            return user
        
        if firebase_uid == "123" and request.email == "john@example.com":
            raise DuplicateUserError()
        else:
            raise UserNotFoundError()
    # Helper method
    def create_user_data(self, name: str | None = None, email: str | None = None):
        return UserResponse(
            id="a686c824-25e6-4704-87a6-651938429111",
            name=name or "Mary",
            email=email or "mary@example.com",
            role="standard"
        )
    
    def get_milestones_by_type(self, child_id, type, firebase_uid, limit):
        if firebase_uid == "123":
            return [self.milestone_data(id="milestone-121", type="weekly_goals")]
        
    def get_milestones(self, child_id, firebase_uid, limit):
        if firebase_uid == "123":
            data = [
                self.milestone_data(id="milestone-123", type="weekly_goal"),
                self.milestone_data(id="milestone-124", type="books_read"),
            ]
            return data
            
        if firebase_uid == "777":
            return []
        
    def get_milestone(self, child_id, milestone_id, firebase_uid):
        if firebase_uid == "123":
            return self.milestone_data(id="milestone-123", type="books_read")
        
    def milestone_data(self, id: str, type: str):
        # Constructs a milestone object
        timestamp = datetime.now(timezone.utc)
        return MilestoneCompletionResponse(
            id=id,
            child_id="child-123",
            milestone_id=id,
            type=type,
            description="Amy read 5 books about elephants",
            completed_at=timestamp,
            reward_url=f'/{id}'
        )                      
            

# app with Facade dependency override (auth overrides are done per test)
@pytest.fixture
def test_app(monkeypatch):
    # Ensures that the test's uid override happens before the auth_current_user's override
    monkeypatch.setenv("ENVIRONMENT", "testing")

    app = create_app(settings=UnitTestingConfig())

    app.dependency_overrides[get_facade] = lambda: FakeFacade()
    yield app
    app.dependency_overrides.clear()

@pytest.fixture
def client(test_app):
    return TestClient(test_app)

#Allow dynamic uid creation for auth dependency overrides
@pytest.fixture
def override_auth(test_app):
    def _override(uid: str):
        async def override():
            return {"uid" : uid}
        test_app.dependency_overrides[auth_current_user] = override
    return _override