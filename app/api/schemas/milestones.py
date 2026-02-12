from pydantic import BaseModel
from datetime import datetime

class CreateMilestone(BaseModel):
    name: str
    description: str
    metric_key: str
    threshold: int

class MilestoneResponse(BaseModel):
    # record of milestone type
    ms_type_id: str
    name: str
    description: str
    metric_key: str
    threshold: int

class MilestoneCompletionResponse(BaseModel):
    # record of completion
    child_id: str
    milestone_id: str
    achieved_at: datetime