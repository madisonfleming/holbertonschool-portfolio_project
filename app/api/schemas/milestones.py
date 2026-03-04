from pydantic import BaseModel
from datetime import datetime

class CreateMilestone(BaseModel):
    # Used for requests to post weekly milestones
    child_id: str
    subject: str


class MilestoneResponse(BaseModel):
    # Used for responses to post weekly milestones and get milestones
    created_at: datetime
    id: str
    name: str
    description: str
    metric_key: str
    threshold: int
    child_id: str
