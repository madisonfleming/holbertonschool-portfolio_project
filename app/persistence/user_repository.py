#!/usr/bin/python3
from app.persistence.repository import Repository

""" 
Set up hardcoded User data for us to use
while the repository is in-memory

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

USERS = {
    user1["id"]: user1,
    user2["id"]: user2,
    user3["id"]: user3,
}

# Uncomment to inspect the User data
# print(USERS)

class UserRepository(Repository):
    def __init__(self):
        self._storage = USERS

    def save(self, obj):
        self._storage[obj.id] = obj

    def get(self, obj_id):
        return self._storage.get(obj_id)

    def get_all(self):
        pass

    def update(self, obj_id, data):
        pass

    def delete(self, obj_id):
        pass

    def get_by_attribute(self, attr_name, attr_value):
        pass
