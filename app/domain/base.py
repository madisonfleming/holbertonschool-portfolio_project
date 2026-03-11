import uuid
from datetime import datetime, timezone

"""
Base class for the common elements of all models
- uuid
- created_at
- updated_at

Accepts optional override so that objects loaded from storage 
can use the model as well as those created with Base
""" 

class Base:
    def __init__(
        self,
        id: str | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        now = datetime.now(timezone.utc)
        self.id = id or str(uuid.uuid4())
        self.created_at = created_at or now
        self.updated_at = updated_at or now

    # Allows every model to update the updated_at timestamp
    def touch(self):
        now = datetime.now(timezone.utc)
        self.updated_at = now

    def to_dict(self):
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
