from app.domain.base import Base
from datetime import date
from app.domain.exceptions import (
    InvalidChildNameError,
    InvalidDateOfBirthError
)


class Child(Base): # gives id, created_at, updated_at
    def __init__(self,
                 name: str,
                 date_of_birth: date,
                 avatar_url: str | None = None
    ):
        super().__init__()
        self.name = name
        self.date_of_birth = date_of_birth
        self.avatar_url = avatar_url

    @property
    def child_id(self):
        return self.id # comes from Base

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Child name must be a string")
        if not value.strip():
            raise InvalidChildNameError()
        self._name = value

    @property
    def date_of_birth(self):
        return self._date_of_birth

    @date_of_birth.setter
    def date_of_birth(self, value):
        if value and not isinstance(value, date):
            raise TypeError("date_of_birth must be a date")
        if value > date.today(): # guards entry of a future date
            raise InvalidDateOfBirthError()
        self._date_of_birth = value
    
    @property
    def age(self):
        today = date.today()
        years = today.year - self.date_of_birth.year

        # adjustment for if birthday in current year hasn't occurred yet
        if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
            years -= 1

        return years


    def to_dict(self):
        data = super().to_dict()
        data.update({
            "id": self.child_id,
            "name": self.name,
            "age": self.age,
            "date_of_birth": self.date_of_birth.isoformat(),
            "avatar_url": self.avatar_url
        })
        return data

# convert data from dict to domain model object. Data required by ChildResponse schema
def from_dict(data: dict) -> Child:
    child = Child(
        name=data["name"],
        date_of_birth=date.fromisoformat(data["date_of_birth"]),
        avatar_url=data["avatar_url"],
        )
    child.id=data["id"]
    return child
