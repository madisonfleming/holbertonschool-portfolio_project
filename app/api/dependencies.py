from app.services.facade import MLBFacade
from app.persistence.sqlalchemy.db import engine

from app.persistence.sqlalchemy.user_repository_sqlalchemy import UserRepositorySQLAlchemy
from app.persistence.sqlalchemy.child_repository_sqlalchemy import ChildRepositorySQLAlchemy
from app.persistence.sqlalchemy.reading_session_repository_sqlalchemy import ReadingSessionRepositorySQLAlchemy
from app.persistence.sqlalchemy.milestone_type_repository_sqlalchemy import MilestoneTypeRepositorySQLAlchemy
from app.persistence.sqlalchemy.milestone_completion_repository_sqlalchemy import MilestoneCompletionRepositorySQLAlchemy
from app.persistence.sqlalchemy.relationship_repository_sqlalchemy import RelationshipRepositorySQLAlchemy
from app.persistence.sqlalchemy.book_repository_sqlalchemy import BookRepositorySQLAlchemy

from app.external.open_library_api import OpenLibraryClient

# milestone_repository = MilestoneTypeRepository() # create instance of type repo
# # create an instance of completion repo + pass in the type instance - Allows completion repo to use methods from type repo
# milestone_completion_repository = MilestoneCompletionRepository(milestone_repository) 

# creates an instance of each repo and passes them to the facade
# which in turn is fed (below) to the router reg's to ensure they all use the same facade instance
facade = MLBFacade(
    user_repository=UserRepositorySQLAlchemy(engine),
    child_repository=ChildRepositorySQLAlchemy(engine),
    reading_session_repository=ReadingSessionRepositorySQLAlchemy(engine),
    milestone_repository=MilestoneTypeRepositorySQLAlchemy(engine),
    milestone_completion_repository=MilestoneCompletionRepositorySQLAlchemy(engine),
    relationship_repository=RelationshipRepositorySQLAlchemy(engine),
    book_repository=BookRepositorySQLAlchemy(engine),
    open_library_api=OpenLibraryClient()
)

def get_facade():
    return facade
