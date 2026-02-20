from pydantic import BaseModel
from datetime import datetime

# TODO: can remove if not required in milestone endpoints
class CreateMilestone(BaseModel):
    name: str
    description: str
    metric_key: str
    threshold: int

class MilestoneTypeResponse(BaseModel):
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

class MilestoneResponse(BaseModel):
    # combines both responses to return to FE. FE gets both objects nested in the response body's object
    milestone: MilestoneTypeResponse
    completion: MilestoneCompletionResponse | None # NOTE: making optional in response to account for WIP milestones
