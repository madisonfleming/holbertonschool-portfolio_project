from dataclasses import dataclass, field
from datetime import datetime
from app.domain.base import Base
from dataclasses import asdict

"""
internal domain representation of a completed milestone, kept separate
from API schemas so the repository works with simple data objects
as opposed the pydantic models

to elaborate slightly, the milestone_completion dataclass will only be used by the
repo and the facade, not the API layer, so we don't need to define
behaviour as we would with the domain models. We do need the
internal domain representation, however
"""
@dataclass
class MilestoneCompletion(Base): # gives id, created_at, updated_at
    child_id: str
    milestone_id: str
    description: str
    completed_at: datetime
    reward_generated_at: datetime | None = None
    reward_url: str | None = None

    id: str = field(init=False)
    created_at: datetime = field(init=False)
    updated_at: datetime = field(init=False)

    def __post_init__(self):
        super().__init__()      # this initialises Base class
    
    def to_dict(self):
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> "MilestoneCompletion":
        obj= cls(
            child_id=data["child_id"],
            milestone_id=data["milestone_id"],
            description=data["description"],
            completed_at=data["completed_at"],
            reward_generated_at=(
                datetime.fromisoformat(data["reward_generated_at"])
                if data["reward_generated_at"] else None
            ),
            reward_url=data["reward_url"],
        )

        obj.id = data["id"]
        obj.created_at = data["created_at"]
        obj.updated_at = data["updated_at"]

        return obj
