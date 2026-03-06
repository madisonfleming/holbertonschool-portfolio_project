from pydantic import BaseModel
from datetime import datetime

class CreateMilestone(BaseModel):
    # Used for requests to post weekly milestones
    child_id: str
    subject: str


class MilestoneResponse(BaseModel):
    # Used for the milestone definitions
    created_at: datetime
    id: str
    name: str
    description: str
    type: str
    threshold: int


class MilestoneCompletionResponse(BaseModel):
    # Used for responses to post weekly milestones and get milestones
    id: str
    child_id: str
    milestone_id: str
    description: str
    completed_at: datetime
    reward_url: str | None