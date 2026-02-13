""" 
Defines the user attributes and methods. Inherits:
- id = uuid
- created_at = timestamp
- updated_at = timestamp
"""

from app.domain.base import Base


class User(Base):
    def __init__(self,
                 name: str,
                 email: str,
                 role: str = "standard",
                 firebase_uid: str | None = None
                 ):
        super().__init__()
        self.name = name
        self.email = email
        self.role = role
        self.firebase_uid = firebase_uid

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

    def update_profile(self, data):
        fields = ['name', 'email']  # Explicitly disallow role update
        for item in data:
            if item in fields:
                setattr(self, item, data[item])
        self.touch()  # sets updated_at attr

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role
        }
