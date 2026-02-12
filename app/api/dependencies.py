from app.services.facade import MLBFacade
from app.persistence.user_repository import UserRepository
from app.persistence.child_repository import ChildRepository
from app.persistence.reading_session_repository import ReadingSessionRepository
from app.persistence.milestone_repository import MilestoneRepository
from app.persistence.milestone_completion_repository import MilestoneCompletionRepository

# creates an instance of each repo and passes them to the facade
# which in turn is fed (below) to the router reg's to ensure they all use the same facade instance
facade = MLBFacade(
    user_repo=UserRepository(),
    child_repo=ChildRepository(),
    session_repo=ReadingSessionRepository(),
    milestone_repo=MilestoneRepository(),
    completion_repo=MilestoneCompletionRepository(),
)

def get_facade():
    return facade
