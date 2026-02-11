#!/usr/bin/python3

from my_little_bookworm.domain.user import User
from my_little_bookworm.persistence.user_repository import UserRepository
from my_little_bookworm.api.v1.schemas.users import CreateUser
from typing import Dict


class MLBFacade:
    def __init__(
        self,
        user_repo: UserRepository,
        child_repo,
        session_repo,
        milestone_repo,
        completion_repo
    ):
        self.user_repo = user_repo
        self.child_repo = child_repo
        self.session_repo = session_repo
        self.milestone_repo = milestone_repo
        self.completion_repo = completion_repo


    # User
    def create_user(self, req: CreateUser) -> Dict:
        """ create a new user (POST /users)"""
        user = User(name=req.name, email=req.email)
        self.user_repo.add(user)
        return user.to_dict()
