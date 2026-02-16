import uuid
from datetime import datetime

RELATIONSHIPS = {
    str(uuid.uuid4()): {
        "user_id": "Mary",
        "child_id": "Bob",
        "role": "owner",
        "invited_by": None,
        "invite_status": None,
        "created_at": datetime.now()
    },
    str(uuid.uuid4()): {
        "user_id": "Mary",
        "child_id": "Sophie",
        "role": "owner",
        "invited_by": None,
        "invite_status": None,
        "created_at": datetime.now()
    }
}

class CarerAccessRepository():
    def __init__(self):
        self._storage = RELATIONSHIPS

    def get(self, obj_id):
        # Which id will be passed in?
        return self._storage[obj_id]

    def get_all(self):
        return list(self._storage.values())

    def grant_access(self, id, relationship):
        self._storage[id] = relationship

    # def revoke_access(self, user_id, child_id):
    #     if obj_id in self._storage:
    #         del self._storage[obj_id]

    def has_role(self, owner_id, child_id, role):
        # # Check access_repo for role associated with owner_id/child_id pair
        # record = self._storage[child_id]
        return True
    

repo = CarerAccessRepository()

id = str(uuid.uuid4())
new_relationship = {
    "user_id": "Steve",
    "child_id": "Bob",
    "role": "parent",
    "invited_by": "Mary",
    "invite_status": "Accepted",
    "created_at": datetime.now()
}

repo.grant_access(id, new_relationship)  # Tests adding a new relationship
print(repo.get(id))  # Tests fetching by relationship id (must be known)