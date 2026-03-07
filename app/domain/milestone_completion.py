from dataclasses import dataclass, field
from datetime import datetime
from app.domain.base import Base
from dataclasses import asdict

"""
internal domain representation of a completed milestone, kept separate
from API schemas so the repository works with simple data objects
as opposed the pydantic models

to elaborate slightly, the book dataclass will only be used by the
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
