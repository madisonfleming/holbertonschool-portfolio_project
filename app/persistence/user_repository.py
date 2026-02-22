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

user4 = {
    "created_at": "2026-02-18 04:39:42.220228",
    "updated_at": "2026-02-18 04:39:42.220228",
    "id": "d686c824-25e6-4704-87a6-651938429111",
    "name": "Andrea",
    "email": "andrea@example.com",
    "role": "standard",
    "firebase_uid": "7UKtP5I8lBbDoO8wVv6WB8Ge03Q2",
}


USERS = {
    user1["firebase_uid"]: user1,
    user2["firebase_uid"]: user2,
    user3["firebase_uid"]: user3,
    user4["firebase_uid"]: user4,

}

# Uncomment to inspect the User data
# print(USERS)

class UserRepository(Repository):
    def __init__(self):
        self._storage = USERS

    def save(self, obj):
        self._storage[obj.firebase_uid] = obj

    def get(self, obj_id):
        return self._storage.get(obj_id)
    
    def get_by_firebase_uid(self, firebase_uid):
        return self._storage[firebase_uid]

    def get_all(self):
        pass

    def update(self, obj_id, data):
        pass

    def delete(self, obj_id):
        pass

    def get_by_attribute(self, attr_name, attr_value):
        pass
