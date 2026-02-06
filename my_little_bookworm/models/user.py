""" 
Defines the user attributes and methods. Inherits:
- id = uuid
- created_at = timestamp
- updated_at = timestamp
"""

from .base import Base


class User(Base):
    def __init__(self):
        super().__init__()
