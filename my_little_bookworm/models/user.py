""" 
Defines the user attributes and methods. Inherits:
- id = uuid
- created_at = timestamp
- updated_at = timestamp
"""

from models.base import Base


class User(Base):
    def __init__(self, name, email, role='standard'):
        super().__init__()
        self.name = name
        self.email = email
        self.role = role

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str):
        if not name:
            raise ValueError("Name must be provided")
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        self._name = name

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email: str):
        if not email:
            raise ValueError("Email must be provided")
        if not isinstance(email, str):
            raise TypeError("Email must be a string")
        self._email = email

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
    # x add all attributes in User class definition
    #   nb - pw not required with Firebase
    # Define methods
    # - updateUser(data)
    # - getLinkedChildren()
    # - getFamilyRoles()
