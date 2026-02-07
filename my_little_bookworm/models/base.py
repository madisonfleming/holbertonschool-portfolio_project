"""
Base class for the common elements of
all models
- uuid
- created_at
- updated_at
"""

import uuid
from datetime import datetime


class Base:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    # Allows every model to update the updated_at timestamp
    def touch(self):
        self.updated_at = datetime.now()
