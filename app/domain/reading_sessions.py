from dataclasses import dataclass
from datetime import datetime

"""
internal domain representation of a reading session, kept separate
from API schemas so the repository works with simple data objects
as opposed the pydantic models

to elaborate slightly, the reading session dataclass will only be used by the
repo and the facade, not the API layer, so we don't need to define
behaviour as we would with the domain models. We do need the
internal domain representation, however

I think with this section, if we wanted to expand its behaviour to track
metrics, like reading session streaks, we might need to introduce a proper
domain model. For MVP this will serve its purpose though

"""
@dataclass
class ReadingSession:
    session_id: str
    child_id: str
    book_id: str
    logged_at: datetime
