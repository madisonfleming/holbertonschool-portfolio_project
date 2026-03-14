from datetime import datetime
import uuid

from sqlalchemy import insert, select
from sqlalchemy.engine import Engine

from app.domain.repositories.relationship_repository import RelationshipRepositoryBase
from app.persistence.sqlalchemy.tables import relationships


class RelationshipRepositorySQLAlchemy(RelationshipRepositoryBase):
    def __init__(self, engine: Engine):
        self.engine = engine

    def get(self, relationship_id: str) -> dict | None:
        # applied with relationship_id but I'm not sure we have a meaningful use for this?
        stmt = select(relationships).where(relationships.c.id == relationship_id)
        with self.engine.begin() as conn:
            row = conn.execute(stmt).mappings().fetchone()

        if row is None:
            return None

        return dict(row)

    # returns the type of relationship betwixt child and user
    # fronties may need this for conditional data exposure
    def get_relationship_type(
        self,
        user_id: str,
        child_id: str
    ) -> dict | None:
        stmt = select(relationships).where(
            relationships.c.user_id == user_id,
            relationships.c.child_id == child_id,
        )
        with self.engine.begin() as conn:
            row = conn.execute(stmt).mappings().fetchone()

        if row is None:
            return None

        return dict(row)

    def create_relationship(
        self,
        user_id: str,
        child_id: str,
        role: str,
        relationship_type: str,
    ) -> str:
        # primary/secondary relationships are modelled here as we aren't
        # modelling relationship in the domains
        # validation should be handled in the facade
        relationship_id = str(uuid.uuid4())
        now = datetime.now()

        values = {
            "id": relationship_id,
            "user_id": user_id,
            "child_id": child_id,
            "role": role,
            "relationship_type": relationship_type,
            "invited_by": None,
            "acceptance_status": "accepted", # default for primary user
            "created_at": now,
            "updated_at": now,
        }

        with self.engine.begin() as conn:
            stmt = insert(relationships).values(values)
            conn.execute(stmt)

        return relationship_id

    def has_role(
        self,
        user_id: str,
        child_id: str,
        role: str
    ) -> bool:
        relationship = self.get_relationship_type(user_id, child_id)
        return relationship is not None and relationship["role"] == role

    # check for role match with multiple roles listed
    # more specific approach for the likes of 'get reading session' where thirdary not allowed
    def has_one_of_roles(
        self,
        user_id: str,
        child_id: str,
        roles: list[str]
    ) -> bool:
        relationship = self.get_relationship_type(user_id, child_id)
        return relationship is not None and relationship["role"] in roles


    def get_children_per_user(self, user_id: str) -> list[dict]:
        # returns a filtered list of relationship dicts by user_id
        stmt = select(relationships).where(relationships.c.user_id == user_id)
        with self.engine.begin() as conn:
            rows = conn.execute(stmt).mappings().fetchall()

        results = []
        for row in rows:
            results.append(dict(row))

        return results

    # check for ANY role association with child
    # applicable for the likes of 'add reading session' where all role types apply
    def has_relationship(
        self,
        user_id: str,
        child_id: str
    ) -> bool:
        relationship = self.get_relationship_type(user_id, child_id)
        return relationship is not None