""" 
This file defines the seeded data for in-memory persistence for the following entities:
- user
- child
- relationship

This dataset supports Swagger testing

Book data added as objects as book repo is not designed for dicts.
"""
from app.domain.books import Book
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

# <--- BOOKS --->
class Bookdata():
    book1 = Book(
        id="d5df0557-4d06-46c8-b4f3-105511e3000a",
        external_id="/works/OL2568879W",
        source="openlibrary",
        title="Where the Wild Things Are",
        author="Maurice Sendak",
        cover_url="https://covers.openlibrary.org/b/id/50842-M.jpg",
    )

    book2 = Book(
        id="d5df0557-4d06-46c8-b4f3-105511e3000b",
        external_id="/works/OL52987W",
        source="openlibrary",
        title="The Very Hungry Caterpillar",
        author="Eric Carle",
        cover_url="https://covers.openlibrary.org/b/id/7835968-M.jpg",
    )

    book3 = Book(
        id="d5df0557-4d06-46c8-b4f3-105511e3000c",
        external_id="/works/OL483391W",
        source="openlibrary",
        title="Charlotte's Web",
        author="E. B. White",
        cover_url="https://covers.openlibrary.org/b/id/8461797-M.jpg",
    )

    BOOKS = {
        book1.id: book1,
        book2.id: book2,
        book3.id: book3,
    }

    def __init__(self):
        self.books = self.BOOKS
