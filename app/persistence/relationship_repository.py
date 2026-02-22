import uuid


""" 
Set up hardcoded Relationship data for us to use
while the repository is in-memory

TO DO: remove hardcoded data after MySQL is connected
"""
# from app.persistence.child_repository import ChildRepository
# from app.persistence.user_repository import UserRepository

# Validate that the hardcoded child and user data is available from here
# child_repo = ChildRepository()
# user_repo = UserRepository()

# print("GET CHILD FROM REL", child_repo.get('e686c824-25e6-4704-87a6-65193842911c'))
# print("GET USER FROM REL", user_repo.get('b433c6ab-fba5-49a9-9d57-99db6b690efc'))

# Mary is the primary user for Susie's child profile
relationship1 = {
        "id": "c686c824-25e6-4704-87a6-651938429232",
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
        "id": "c686c824-25e6-4704-87a6-651938429233",
        "user_id": "a686c824-25e6-4704-87a6-651938429111",
        "child_id": "e686c824-25e6-4704-87a6-651938429112",
        "role": "primary",
        # "invited_by": None,
        # "invite_status": None,
        # "created_at": "2026-02-18 04:39:42.220228",
        # "updated_at": "2026-02-18 04:39:42.220228"
}

RELATIONSHIPS = {
    relationship1["id"]: relationship1,
    relationship2["id"]: relationship2,
}
# Uncomment to inspect hardcoded data
# print(RELATIONSHIPS)

# RelationshipRepository doesn't inherit from Repository because
# relationship wasn't modeled as a first-class domain
# It only has the methods it has needed so far
class RelationshipRepository():
    def __init__(self):
        self._storage = RELATIONSHIPS

    def get(self, obj_id):
        # Which id will be passed in?
        return self._storage[obj_id]

    def get_all_child_ids(self):
        return list(self._storage.values())
    

    def add_member(self, user_id, child_id, role):
        # This method needs to handle setting up the relationship
        # data construct, because there's no domain model to do it for us
        # For now it only models what's needed in create_child in the facade class
        # TO DO:
        #  - Work out how to handle non-primary user_ids
        #  - Add all of the attributes given in the design doc
        member_id = str(uuid.uuid4())
        relationship = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "child_id": child_id,
            "role": role
        }
        self._storage[member_id] = relationship
        return member_id

    # def revoke_access(self, user_id, child_id):
    #     if obj_id in self._storage:
    #         del self._storage[obj_id]

    # def has_role(self, owner_id, child_id, role):
    #     # # Check access_repo for role associated with owner_id/child_id pair
    #     # record = self._storage[child_id]
    #     return True
    
    def get_children_per_user(self, user_id):
        # returns a filtered list of relationship dicts by user_id
        result = []
        for rel in self._storage.values():
            if rel["user_id"] == user_id:
                result.append(rel)
        return result

"""
This section is to test out the relationship repo methods without having to touch the facade

Uncomment the block to test each method

"""
# repo = RelationshipRepository()

# user_id = "a686c824-25e6-4704-87a6-651938429111"  # Mary
# child_id = "e686c824-25e6-4704-87a6-651938429112"  # Billy
# role = "primary"

# # Full data model - not necessary yet! Kept for future-me
# # new_relationship = {
# #     "created_at": "2026-02-18 04:39:42.220228",
# #     "updated_at": "2026-02-18 04:39:42.220228",
# #     "id": id,
# #     "user_id": "a686c824-25e6-4704-87a6-651938429111",
# #     "child_id": "e686c824-25e6-4704-87a6-651938429112",
# #     "role": "parent",
# #     "invited_by": None,
# #     "invite_status": None,
# # }

# relationship_id = repo.add_member(user_id, child_id, role)  # Tests adding a new relationship
# for r in RELATIONSHIPS:
#     print(RELATIONSHIPS[r])
# print(repo.get(relationship_id))  # Tests fetching by relationship id (must be known)