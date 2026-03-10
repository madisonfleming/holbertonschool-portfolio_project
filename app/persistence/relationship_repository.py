from app.domain.repositories.relationship_repository import RelationshipRepositoryBase

from datetime import datetime
import uuid
from app.persistence.in_memory_seed import Relationshipdata

# RelationshipRepository doesn't inherit from Repository because
#   relationship wasn't modeled as a first-class domain

class RelationshipRepository(RelationshipRepositoryBase):
    def __init__(self):
        self._storage = Relationshipdata().relationships

    def get(self, relationship_id: str) -> dict:
        # applied with relationship_id but I'm not sure we have a meaningful use for this?  
        return self._storage[relationship_id]

    # returns the type of relationship betwixt child and user
    # fronties may need this for conditional data exposure
    def get_relationship_type(
        self,
        user_id: str,
        child_id: str,
    ) -> dict | None:
        return self._find_relationship(user_id, child_id)

    def create_relationship(
        self,
        user_id: str,
        child_id: str,
        role: str,
        relationship_type:str,
    ) -> str:
        # primary/secondary relationships are modelled here as we aren't
        # modelling relationship in the domains
        # validation should be handled in the facade
        relationship_id = str(uuid.uuid4())
        now = datetime.utcnow()

        relationship = {
            "id": relationship_id,
            "user_id": user_id,
            "child_id": child_id,
            "role": role,
            "relationship_type": relationship_type,
            "invited_by": None,
            "invite_status": "accepted", # default for primary user
            "created_at": now,
            "updated_at": now,
        }
        self._storage[relationship_id] = relationship
        return relationship_id

    # def revoke_access(self, user_id, child_id):
    #     if obj_id in self._storage:
    #         del self._storage[obj_id]

    # Check access_repo for particular role associated with owner_id/child_id pair
    def has_role(
        self,
        user_id: str,
        child_id: str,
        role: str
    ) -> bool:
        relationship = self._find_relationship(user_id, child_id)
        return relationship is not None and relationship["role"] == role
    
    # check for role match with multiple roles listed
    # more specific approach for the likes of 'get reading session' where thirdary not allowed
    def has_one_of_roles(
        self,
        user_id: str,
        child_id: str,
        roles: list[str],
    ) -> bool:
        relationship = self._find_relationship(user_id, child_id)
        return relationship is not None and relationship["role"] in roles

    
    def get_children_per_user(self, user_id: str) -> list[dict]:
        # returns a filtered list of relationship dicts by user_id
        return self._find_relationships_by_user(user_id)

    # check for ANY role association with child
    # applicable for the likes of 'add reading session' where all role types apply
    def has_relationship(
        self,
        user_id: str,
        child_id: str,
    ) -> bool:
        return self._find_relationship(user_id, child_id) is not None
    
    def _find_relationship(
        self,
        user_id: str,
        child_id: str,
    ) -> dict | None:
        for relationship in self._storage.values():
            if relationship["user_id"] == user_id and relationship["child_id"] == child_id:
                return relationship
        return None

    def _find_relationships_by_user(self, user_id: str) -> list[dict]:
        return [
            rel for rel in self._storage.values()
            if rel["user_id"] == user_id
        ]
