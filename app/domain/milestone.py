from app.domain.base import Base

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
    def name(self, value: str):
        if not value or not isinstance(value, str):
            raise ValueError("Milestone name must be a non-empty string")
        self._name = value

    @property
    def threshold(self):
        return self._threshold

    @threshold.setter
    def threshold(self, value: int):
        if not isinstance(value, int) or value < 1:
            raise ValueError("Threshold must be a positive int")
        self._threshold = value

    def to_dict(self):
        return {
            "ms_type_id": self.id,
            "name": self.name,
            "description": self.description,
            "metric_key": self.metric_key,
            "threshold": self.threshold,
        }
