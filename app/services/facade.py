#!/usr/bin/python3

from app.domain.user import User
from app.domain.child import Child
from app.persistence.user_repository import UserRepository
from app.persistence.child_repository import ChildRepository
from app.persistence.carer_access_repository import CarerAccessRepository
from app.api.schemas.users import CreateUser
from typing import Dict
import uuid
from datetime import datetime


class MLBFacade:
    def __init__(
        self,
        user_repo: UserRepository,
        child_repo: ChildRepository,
        access_repo: CarerAccessRepository,
        session_repo,
        milestone_repo,
        completion_repo
    ):
        self.user_repo = user_repo
        self.child_repo = child_repo
        self.access_repo = access_repo
        self.session_repo = session_repo
        self.milestone_repo = milestone_repo
        self.completion_repo = completion_repo

    # User
    def create_user(self, req: CreateUser) -> Dict:
        """ create a new user (POST /users)"""
        user = User(name=req.name, email=req.email)
        self.user_repo.add(user)
        return user.to_dict()

    # Child
    def create_child(self) -> Dict:
        """ Example of what the create_child facade layer might look like
        
        Note that the data structure is pure Python, and in reality it would be send by a FastAPI request
        """
        id = str(uuid.uuid4())
        user_id = str(uuid.uuid4())

        data = {
            'name': 'Bob',
            'date_of_birth': '2023-12-05'
        }

        child = Child(data)
        self.child_repo.add(child)

        relationship = {
            "user_id": user_id,
            "child_id": child.id,
            "role": "owner",
            "invited_by": None,
            "invite_status": None,
            "created_at": datetime.now()
        }
        self.access_repo.grant_access(id, relationship)
        return child.to_dict()
    
class ChildSharingService(MLBFacade):
    """ OPTION 1
    Handle relationship logic between the Facade and Service layers
    - Don't model the relationship as a separate domain entity
    - Relies on adding "owner_id" attribute to Child model

    Database - join table
    Repository - CarerAccessRepository
    Facade - separate class to handle relationships

    """

    def share_child(self, owner_id, child_id, target_user_id, role):
        if not self.access_repo.has_role(owner_id, child_id, "owner"):
            raise PermissionError("Only owner can share")
        
        self.access_repo.grant_access(
                user_id = target_user_id,
                child_id = child_id,
                role = role
        )