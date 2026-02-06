""" 
Defines the user attributes and methods. Inherits:
- id = uuid
- created_at = timestamp
- updated_at = timestamp
"""

from models.base import Base


class User(Base):
    def __init__(self, role='standard'):
        super().__init__()
        self.role = role

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, role: str):
        if not role:
            self._role = 'standard'
        if not isinstance(role, str):
            raise TypeError("Role must be a string")
        if role != 'admin':
            self._role = 'standard'
        if role == 'admin':
            self._role = role

    # TO-DO:
    # x validate role
    # x test validations
    # - updateUser(data)
    # - getLinkedChildren()
    # - getFamilyRoles()
