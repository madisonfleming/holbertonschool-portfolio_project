from dataclasses import dataclass
from datetime import datetime
from app.domain.base import Base

"""
internal domain representation of a stored book, kept separate
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
    metric_key: str
    completed_at: datetime
    reward_generated_at: datetime | None = None
    reward_url: str | None = None
