from app.services.facade import MLBFacade
from app.persistence.user_repository import UserRepository
from app.persistence.child_repository import ChildRepository
from app.persistence.reading_session_repository import ReadingSessionRepository
from app.persistence.milestone_repository import MilestoneTypeRepository
from app.persistence.milestone_completion_repository import MilestoneCompletionRepository
from app.persistence.relationship_repository import RelationshipRepository
from app.persistence.book_repository import BookRepository
from app.external.open_library_api import OpenLibraryClient

# creates an instance of each repo and passes them to the facade
# which in turn is fed (below) to the router reg's to ensure they all use the same facade instance
facade = MLBFacade(
    user_repository=UserRepository(),
    child_repository=ChildRepository(),
    reading_session_repository=ReadingSessionRepository(),
    milestone_repository=MilestoneTypeRepository(),
    milestone_completion_repository=MilestoneCompletionRepository(),
    relationship_repository=RelationshipRepository(),
    book_repository=BookRepository(),
    open_library_api=OpenLibraryClient()
)

def get_facade():
    return facade
