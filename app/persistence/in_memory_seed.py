""" 
This file defines the seeded data for in-memory persistence for the following entities:
- user
- child
- relationship

This dataset supports Swagger testing
"""
# <--- USER DATA --->

class Userdata():
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

    USERS = {
            user1["firebase_uid"]: user1,
            user2["firebase_uid"]: user2,
            user3["firebase_uid"]: user3,
            user4["firebase_uid"]: user4,
        }
    
    def __init__(self):
        self.users = self.USERS

class Childdata():
    child1 = {
        "created_at": "2026-02-18 04:39:42.220228",
        "updated_at": "2026-02-18 04:39:42.220228",
        'id': 'e686c824-25e6-4704-87a6-651938429111',
        'name': 'Susie',
        'date_of_birth': '2023-12-05',
        'age': 2,
        'avatar_url': "/avatars/mlb-avatar-robot.png"
        }

    child2 = {
        "created_at": "2026-02-18 04:39:42.220228",
        "updated_at": "2026-02-18 04:39:42.220228",
        'id': 'e686c824-25e6-4704-87a6-651938429112',
        'name': 'Billy',
        'date_of_birth': '2024-07-01',
        'age': 1,
        'avatar_url': "/avatars/mlb-avatar-apple.png"
        }

    child3 = {
        "created_at": "2026-02-18 04:39:42.220228",
        "updated_at": "2026-02-18 04:39:42.220228",
        'id': 'e686c824-25e6-4704-87a6-651938429113',
        'name': 'Tom',
        'date_of_birth': '2025-01-29',
        'age': 1,
        'avatar_url': "/avatars/mlb-avatar-bee.png"
        }

    child4 = {
        "created_at": "2026-02-18 04:39:42.220228",
        "updated_at": "2026-02-18 04:39:42.220228",
        'id': '123',
        'name': 'Amy',
        'date_of_birth': '2025-01-29',
        'age': 1,
        'avatar_url': "/avatars/mlb-avatar-sun.png"
        }

    CHILDREN = {
        child1["id"]: child1,
        child2["id"]: child2,
        child3["id"]: child3,
        child4["id"]: child4,
    }
    def __init__(self):
        self.children = self.CHILDREN

# <--- RELATIONSHIPS --->
class Relationshipdata():

# Mary is the primary user for Susie's child profile
    relationship1 = {
            "id": "c686c824-25e6-4704-87a6-651938429231",
            "user_id": "a686c824-25e6-4704-87a6-651938429111",
            "child_id": "e686c824-25e6-4704-87a6-651938429111",
            "role": "primary",
            # "invited_by": None,
            # "invite_status": None,
            # "created_at": "2026-02-18 04:39:42.220228",
            # "updated_at": "2026-02-18 04:39:42.220228"
    }
    # Mary is the primary user for Billy's child profile
    relationship2 = {
            "id": "c686c824-25e6-4704-87a6-651938429232",
            "user_id": "a686c824-25e6-4704-87a6-651938429111",
            "child_id": "e686c824-25e6-4704-87a6-651938429112",
            "role": "primary",
            # "invited_by": None,
            # "invite_status": None,
            # "created_at": "2026-02-18 04:39:42.220228",
            # "updated_at": "2026-02-18 04:39:42.220228"
    }

    # For FE testing: John Doe has a legit firebase uid. Child is Tom.
    relationship3 = {
            "id": "c686c824-25e6-4704-87a6-651938429233",
            "user_id": "d686c824-25e6-4704-87a6-651938429111",
            "child_id": "e686c824-25e6-4704-87a6-651938429113",
            "role": "primary",
            # "invited_by": None,
            # "invite_status": None,
            # "created_at": "2026-02-18 04:39:42.220228",
            # "updated_at": "2026-02-18 04:39:42.220228"
    }

    # For Swagger testing
    # Mary is the primary user for Amy's child profile
    relationship4 = {
            "id": "c686c824-25e6-4704-87a6-651938429234",
            "user_id": "a686c824-25e6-4704-87a6-651938429111",
            "child_id": "123",
            "role": "primary",
            # "invited_by": None,
            # "invite_status": None,
            # "created_at": "2026-02-18 04:39:42.220228",
            # "updated_at": "2026-02-18 04:39:42.220228"
    }

    RELATIONSHIPS = {
        relationship1["id"]: relationship1,
        relationship2["id"]: relationship2,
        relationship3["id"]: relationship3,
        relationship4["id"]: relationship4,
    }

    def __init__(self):
        self.relationships = self.RELATIONSHIPS