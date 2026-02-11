from my_little_bookworm.services.facade import MLBFacade
from my_little_bookworm.persistence.user_repository import UserRepository
from my_little_bookworm.persistence.child_repository import ChildRepository
from my_little_bookworm.persistence.reading_session_repository import ReadingSessionRepository
from my_little_bookworm.persistence.milestone_repository import MilestoneRepository
from my_little_bookworm.persistence.milestone_completion_repository import MilestoneCompletionRepository

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
