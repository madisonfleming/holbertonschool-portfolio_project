from app.services.facade import MLBFacade
from app.persistence.user_repository import UserRepository
from app.persistence.child_repository import ChildRepository
from app.persistence.reading_session_repository import ReadingSessionRepository
from app.persistence.milestone_repository import MilestoneRepository
from app.persistence.milestone_completion_repository import MilestoneCompletionRepository
from app.persistence.relationship_repository import RelationshipRepository

# creates an instance of each repo and passes them to the facade
# which in turn is fed (below) to the router reg's to ensure they all use the same facade instance
facade = MLBFacade(
    user_repository=UserRepository(),
    child_repository=ChildRepository(),
    reading_session_repository=ReadingSessionRepository(),
    milestone_repository=MilestoneRepository(),
    milestone_completion_repository=MilestoneCompletionRepository(),
    relationship_repository=RelationshipRepository(),
)

def get_facade():
    return facade
