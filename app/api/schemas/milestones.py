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

    @classmethod
    def from_domain(cls, milestone):     # cls is MilestoneResponse
        return cls(
            created_at=milestone.created_at,
            id=milestone.id,
            name=milestone.name,
            description=milestone.description,
            type=milestone.type,
            threshold=milestone.threshold,
        )

class MilestoneCompletionResponse(BaseModel):
    # Used for responses to post weekly milestones and get milestones
    # Q: do we need/want to return type?
    id: str
    child_id: str
    milestone_id: str
    description: str
    completed_at: datetime
    reward_url: str | None

    @classmethod
    def from_domain(cls, milestone):     # cls is MilestoneCompletionResponse
        return cls(
            id=milestone.id,
            child_id=milestone.child_id,
            milestone_id=milestone.milestone_id,
            description=milestone.description,
            completed_at=milestone.completed_at,
            reward_url=milestone.reward_url,
        )
