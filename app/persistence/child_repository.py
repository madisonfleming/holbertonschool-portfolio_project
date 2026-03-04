#!/usr/bin/python3

from app.persistence.repository import Repository
from app.domain.child import Child
from app.persistence.in_memory_seed import Childdata

class ChildRepository(Repository):
    def __init__(self):
        self._storage = Childdata().children

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

