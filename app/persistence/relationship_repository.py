import uuid
from app.persistence.in_memory_seed import Relationshipdata
# Uncomment to inspect hardcoded data
# print(RELATIONSHIPS)

# RelationshipRepository doesn't inherit from Repository because
# relationship wasn't modeled as a first-class domain
# It only has the methods it has needed so far
class RelationshipRepository():
    def __init__(self):
        self._storage = Relationshipdata().relationships

    def get(self, obj_id):
        # Which id will be passed in?
        return self._storage[obj_id]

    # returns the type of relationship betwixt child and user
    # fronties may need this for conditional data exposure
    def get_relationship(self, user_id, child_id):
        for relationship in self._storage.values():
            if relationship["user_id"] == user_id and relationship["child_id"] == child_id:
                return relationship
        return None


    def get_all_child_ids(self):
        return list(self._storage.values())
    

    def add_member(self, user_id, child_id, role, relationship_type):
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
            "role": role,
            "relationship_type": relationship_type 
        }
        self._storage[member_id] = relationship
        return member_id

    # def revoke_access(self, user_id, child_id):
    #     if obj_id in self._storage:
    #         del self._storage[obj_id]

    # Check access_repo for particular role associated with owner_id/child_id pair
    def has_role(
        self,
        user_id: str,
        child_id: str,
        role: str
    ):
        for relationship in self._storage.values():
            if relationship["user_id"] == user_id and relationship["child_id"] == child_id:
                return relationship["role"] == role     # bool
        return False
    
    # check for role match with multiple roles listed
    # more specific approach for the likes of 'get reading session' where thirdary not allowed
    def has_one_of_roles(
        self,
        user_id: str,
        child_id: str,
        roles: list[str]
    ):
        for relationship in self._storage.values():
            if relationship["user_id"] == user_id and relationship["child_id"] == child_id:
                return relationship["role"] in roles    # bool
        return False
    
    def get_children_per_user(self, user_id):
        # returns a filtered list of relationship dicts by user_id
        result = []
        for rel in self._storage.values():
            if rel["user_id"] == user_id:
                result.append(rel)
        return result


    # check for ANY role association with child
    # applicable for the likes of 'add reading session' where all role types apply
    def has_relationship(
        self,
        user_id: str,
        child_id: str,
    ):
        for relationship in self._storage.values():
            if relationship["user_id"] == user_id and relationship["child_id"] == child_id:
                return True
        return False


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