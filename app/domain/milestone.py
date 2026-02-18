from app.domain.base import Base
from app.domain.exceptions import (
    InvalidMilestoneNameError,
    InvalidMilestoneDescriptionError,
    InvalidMilestoneThresholdError,
    InvalidMetricKeyError
)

class Milestone(Base): # gives id, created_at, updated_at
    def __init__(self,
                name: str,
                description: str,
                metric_key: str,
                threshold: int
    ):
        super().__init__()
        self.name = name # ie "Read 100 Books"
        self.description = description # bit of explanatory text
        self.metric_key = metric_key # books_read, sessions_logged, streak_days. not active but could be.
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
    def description(self):
        return self._description
    
    @description.setter
    def description(self, value:str):
        if not isinstance(value, str):
            raise TypeError("Description must be a string")
        if not value.strip():
            raise InvalidMilestoneDescriptionError()
        self._description = value

    @property
    def metric_key(self):
        return self._metric_key

    @metric_key.setter
    def metric_key(self, value:str):
        if not isinstance(value, str):
            raise TypeError("Metric key must be a string")
        if not value.strip():
            raise InvalidMetricKeyError()
        self._metric_key = value

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
        return {
            "ms_type_id": self.id,
            "name": self.name,
            "description": self.description,
            "metric_key": self.metric_key,
            "threshold": self.threshold
        }
