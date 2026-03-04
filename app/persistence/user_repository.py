#!/usr/bin/python3
from app.persistence.repository import Repository
from app.domain.user import User
from app.persistence.in_memory_seed import Userdata

class UserRepository(Repository):
    def __init__(self):
        self._storage = Userdata().users

    def save(self, user):
        self._storage[user.firebase_uid] = user.to_dict() # save by key=firebase_uid in a dict

    def get(self, obj_id):
        return self._storage.get(obj_id)
    
    def get_by_firebase_uid(self, firebase_uid):
        data = self._storage.get(firebase_uid)
        if data is None:
            return None
        return User.from_dict(data) # converts from dict to User object
    
    # returns a user obj by email address (if found)
    def get_by_email(self, email: str):
        for data in self._storage.values():
            if data["email"].lower() == email.lower():
                return User.from_dict(data)
        return None

    def get_all(self):
        pass

    def update(self, obj_id, data):
        pass

    def delete(self, obj_id):
        pass

    def get_by_attribute(self, attr_name, attr_value):
        pass
