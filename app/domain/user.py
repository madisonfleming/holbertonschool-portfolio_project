""" 
Defines the user attributes and methods. Inherits:
- id = uuid
- created_at = timestamp
- updated_at = timestamp
"""
from datetime import datetime

from app.domain.base import Base
from app.domain.exceptions import (
    InvalidUserNameError,
    InvalidEmailError
)


class User(Base):
    def __init__(
        self,
        name: str,
        email: str,
        role: str = "standard",
        firebase_uid: str | None = None,
        id: str | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)
        self.name = name
        self.email = email
        self.role = role
        self.firebase_uid = firebase_uid

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str):
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        if not name.strip():
            raise InvalidUserNameError()
        self._name = name

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email: str):
        if not isinstance(email, str):
            raise TypeError("Email must be a string")
        if not email.strip():
            raise InvalidEmailError()
        self._email = email

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, role: str):
        if not role:
            self._role = "standard"
        if not isinstance(role, str):
            raise TypeError("Role must be a string")
        if role != "admin":
            self._role = "standard"
        if role == "admin":
            self._role = role

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "firebase_uid": self.firebase_uid
        })
        return data

    # converts hardcoded data from dict to domain model object
    @classmethod
    def from_dict(cls, data: dict) -> "User":
        created = data["created_at"]
        if isinstance(created, str):
            created = datetime.fromisoformat(created)

        updated = data["updated_at"]
        if isinstance(updated, str):
            updated = datetime.fromisoformat(updated)

        return cls(
            id=data["id"],
            name=data["name"],
            email=data["email"],
            role=data["role"],
            firebase_uid=data.get("firebase_uid"),
            created_at=created,
            updated_at=updated,
            )
