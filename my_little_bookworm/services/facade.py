#!/usr/bin/python3

from app.domain.user import User
from app.persistence.user_repository import UserRepository
from app.api.schemas.users import CreateUser
from typing import Dict


class MLBFacade:
    def __init__(self, repo: UserRepository):
        self.user_repo = repo

    # User
    def create_user(self, req: CreateUser) -> Dict:
        """ create a new user (POST /users)"""
        user = User(name=req.name, email=req.email)
        self.user_repo.add(user)
        return user.to_dict()
