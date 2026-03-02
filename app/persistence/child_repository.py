#!/usr/bin/python3

from app.persistence.repository import Repository
from app.domain.child import Child

""" 
Set up hardcoded Child data for us to use
while the repository is in-memory

TO DO: remove hardcoded data after MySQL is connected
"""

child1 = {
    "created_at": "2026-02-18 04:39:42.220228",
    "updated_at": "2026-02-18 04:39:42.220228",
    'id': 'e686c824-25e6-4704-87a6-651938429111',
    'name': 'Susie',
    'date_of_birth': '2023-12-05',
    'age': 2,
    'avatar_url': None
    }

child2 = {
    "created_at": "2026-02-18 04:39:42.220228",
    "updated_at": "2026-02-18 04:39:42.220228",
    'id': 'e686c824-25e6-4704-87a6-651938429112',
    'name': 'Billy',
    'date_of_birth': '2024-07-01',
    'age': 1,
    'avatar_url': None
    }

child3 = {
    "created_at": "2026-02-18 04:39:42.220228",
    "updated_at": "2026-02-18 04:39:42.220228",
    'id': 'e686c824-25e6-4704-87a6-651938429113',
    'name': 'Tom',
    'date_of_birth': '2025-01-29',
    'age': 1,
    'avatar_url': None
    }

child4 = {
    "created_at": "2026-02-18 04:39:42.220228",
    "updated_at": "2026-02-18 04:39:42.220228",
    'id': '123',
    'name': 'Amy',
    'date_of_birth': '2025-01-29',
    'age': 1,
    'avatar_url': None
    }

CHILDREN = {
    child1["id"]: child1,
    child2["id"]: child2,
    child3["id"]: child3,
    child4["id"]: child4,
}

# Uncomment to inspect the Child data
# print(CHILDREN)

class ChildRepository(Repository):
    def __init__(self):
        self._storage = CHILDREN

    def save(self, child):
        self._storage[child.id] = child.to_dict()

    def get(self, child_id):
        data = self._storage.get(child_id)
        return Child.from_dict(data)

    def get_all(self):
        # Not needed on child_repository
        # - will be implemented on relationship_repository
        pass

    def get_by_attribute(self, attr, value):
        return None

    def update(self, id, data):
        pass

    def delete(self, id):
        pass

    def get_by_ids(self, child_ids):
        # child_ids: a list of child ids
        # returns: a list of child objects
        result = []
        for child_id in child_ids:
            child = self.get(child_id)
            if child:
                result.append(child)
        return result

"""
This section is to test out the repo methods without having to touch the facade

To run the tests:
- uncomment the section below
- cd /holbertonschool-portfolio_project
- python -m app.persistence.child_repository
"""
# # Uncomment the whole section for testing without the facade
# import uuid
# from datetime import date, datetime
# from app.domain.child import Child

# child_repo = ChildRepository()

# # Add a new child to the database with .save(child)

# new_child = Child("Michael", date(2024, 5, 1))
# # print(new_child.to_dict())

# child_repo.save(new_child)

# # for c in CHILDREN:
# #     print(CHILDREN[c])

# # child_1 = child1["id"]
# # child_2 = new_child.id

# # Fetch a child from the database with .get(child_id)

# print("GET Child 1:", child_repo.get(child1["id"]))

