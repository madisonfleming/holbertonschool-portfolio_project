#!/usr/bin/python3
from app.persistence.repository import Repository
from app.domain.user import User

""" 
Set up hardcoded User data for us to use
while the repository is in-memory
This repo handles conversion from hardcoded dicts to User objects
All users are currently saved with key=firebase_uid

TO DO: remove hardcoded data after MySQL is connected
"""

user1 = {
    "created_at": "2026-02-18 04:39:42.220228",
    "updated_at": "2026-02-18 04:39:42.220228",
    "id": "a686c824-25e6-4704-87a6-651938429111",
    "name": "Mary",
    "email": "mary@example.com",
    "role": "standard",
    "firebase_uid": "123",
    }

user2 = {
    "created_at": "2026-02-18 04:39:42.220228",
    "updated_at": "2026-02-18 04:39:42.220228",
    "id": "b686c824-25e6-4704-87a6-651938429111",
    "name": "John",
    "email": "john@example.com",
    "role": "standard",
    "firebase_uid": "456",
    }

user3 = {
    "created_at": "2026-02-18 04:39:42.220228",
    "updated_at": "2026-02-18 04:39:42.220228",
    "id": "c686c824-25e6-4704-87a6-651938429111",
    "name": "Charlotte",
    "email": "charlotte@example.com",
    "role": "standard",
    "firebase_uid": "789",
    }

# For Testing: This user has a legit firebase uid
user4 = {
    "created_at": "2026-02-18 04:39:42.220228",
    "updated_at": "2026-02-18 04:39:42.220228",
    "id": "d686c824-25e6-4704-87a6-651938429111",
    "name": "John",
    "email": "john_doe@example.com",
    "role": "standard",
    "firebase_uid": "7UKtP5I8lBbDoO8wVv6WB8Ge03Q2",
    }

# Simple uid for Swagger testing
user5 = {
    "created_at": "2026-02-18 04:39:42.220228",
    "updated_at": "2026-02-18 04:39:42.220228",
    "id": "123",
    "name": "Sam",
    "email": "123@example.com",
    "role": "standard",
    "firebase_uid": "123",
}

USERS = {
    user1["firebase_uid"]: user1,
    user2["firebase_uid"]: user2,
    user3["firebase_uid"]: user3,
    user4["firebase_uid"]: user4,
    user5["firebase_uid"]: user5,
}

# Uncomment to inspect the User data
# print(USERS)

class UserRepository(Repository):
    def __init__(self):
        self._storage = USERS

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
