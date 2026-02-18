import uuid
from datetime import datetime, timezone

"""
Base class for the common elements of all models
- uuid
- created_at
- updated_at
""" 

class Base:
    def __init__(self):
        now = datetime.now(timezone.utc)
        self.id = str(uuid.uuid4())
        self.created_at = now
        self.updated_at = now

    # Allows every model to update the updated_at timestamp
    def touch(self):
        self.updated_at = datetime.now()
