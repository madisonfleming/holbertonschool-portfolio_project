from app.domain.base import Base
from app.domain.exceptions import (
    InvalidMilestoneNameError,
    InvalidMilestoneDescriptionError,
    InvalidMilestoneThresholdError,
    InvalidMetricKeyError
)

class MilestoneType(Base): # gives id, created_at, updated_at
    def __init__(self,
                name: str,
                type: str,
                threshold: int,
                id=None,
                subject: str | None = None,
    ):
        if id is not None:
            self.id = id

        super().__init__()
        self.name = name # ie "Read 100 Books"
        self.subject = subject # of weekly goal milestones
        self.type = type # books_read, sessions_logged, streak_days. not active but could be.
        self.threshold = threshold # number required to achieve milestone

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise InvalidMilestoneNameError()
        if value.strip() == "":
            raise InvalidMilestoneNameError()
        self._name = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value:str):
        if not isinstance(value, str):
            raise TypeError("Metric key must be a string")
        if not value.strip():
            raise InvalidMetricKeyError()
        self._type = value

    @property
    def threshold(self):
        return self._threshold

    @threshold.setter
    def threshold(self, value: int):
        if value is None or value == "":
            raise InvalidMilestoneThresholdError()
        if not isinstance(value, int):
            raise ValueError("Threshold must be an int")
        if value < 1:
            raise InvalidMilestoneThresholdError()
        self._threshold = value

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "subject": self.subject,
            "type": self.type,
            "threshold": self.threshold,
        })
        return data
