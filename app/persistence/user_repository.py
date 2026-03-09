#!/usr/bin/python3
from app.domain.repositories.user_repository import UserRepositoryBase
from app.domain.user import User
from app.persistence.in_memory_seed import Userdata

class UserRepository(UserRepositoryBase):
    def __init__(self):
        self._storage = Userdata().users

    def save(self, user) -> None:
        self._storage[user.firebase_uid] = user.to_dict() # save by key=firebase_uid in a dict

    def get(self, obj_id) -> User | None:
        return self._storage.get(obj_id)
    
    def get_by_firebase_uid(self, firebase_uid) -> User | None:
        data = self._storage.get(firebase_uid)
        if data is None:
            return None
        return User.from_dict(data) # converts from dict to User object
    
    # returns a user obj by email address (if found)
    def get_by_email(self, email: str) -> User | None:
        for data in self._storage.values():
            if data["email"].lower() == email.lower():
                return User.from_dict(data)
        return None
