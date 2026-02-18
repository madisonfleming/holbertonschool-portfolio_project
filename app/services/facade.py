#!/usr/bin/python3

from app.domain.user import User
from app.domain.child import Child

from app.persistence.user_repository import UserRepository
from app.persistence.child_repository import ChildRepository
from app.persistence.reading_session_repository import ReadingSessionRepository
from app.persistence.milestone_repository import MilestoneRepository
from app.persistence.milestone_completion_repository import MilestoneCompletionRepository
from app.persistence.relationship_repository import RelationshipRepository #----->UPDATE this when join method completed

#from app.api.schemas.users import CreateUser
from app.api.schemas.children import CreateChild, ChildResponse

from app.domain.exceptions import InvalidChildNameError 
#from app.services.exceptions import



class MLBFacade:
    def __init__(
        self,
        user_repository: UserRepository,
        child_repository: ChildRepository,
        reading_session_repository: ReadingSessionRepository,
        milestone_repository: MilestoneRepository,
        milestone_completion_repository: MilestoneCompletionRepository,
        relationship_repository: RelationshipRepository #----->UPDATE this when join method completed
    ):
        self.user_repository = user_repository
        self.child_repository = child_repository
        self.reading_session_repository = reading_session_repository
        self.milestone_repository = milestone_repository
        self.milestone_completion_repository = milestone_completion_repository
        self.relationship_repository = relationship_repository #----->UPDATE this when join method completed



    # <--- CHILD --->
    
    def create_child(
        self,
        request: CreateChild,
        firebase_uid: str
    ):
        if not request.name.strip():    # validate request
            raise InvalidChildNameError("Child name must not be empty")
        
        # create domain model
        child = Child(
            name=request.name,
            date_of_birth=request.date_of_birth
        )
        
        # save domain model to db
        saved_child = self.child_repository.save(child)
        
        # ----->TO DO: get_by_firebase_uid to user_repository
        # access user's ID via firebase ID
        user = self.user_repository.get_by_firebase_uid(firebase_uid)
        user_id = user.id

        # example creation of familyMember join
        # ----->assumes existence of relationship_repo w/ add_member method
        self.relationship_repository.add_member(
            user_id=user_id,
            child_id=saved_child.id,
            role="parent" # assuming parent default given they are creating child
        )

        return ChildResponse.from_domain(saved_child)   # convert domain model to response schema

    def get_children(self, firebase_uid: str):
        
        # ----->TO DO: get_by_firebase_uid to user_repository
        # access user's ID via firebase ID
        user = self.user_repository.get_by_firebase_uid(firebase_uid)
        if user is None:
            raise UserNotFoundError()
        user_id = user.id

        # fetch/retrieve linked children
        # doesn't throw error if children = 0, should allow empty Dashy
        children = self._get_linked_children(user_id)

        return [ChildResponse.from_domain(child) for child in children]

    def get_child(
        self,
        child_id,
        firebase_uid
    ):
        # access user's ID via firebase ID
        user = self.user_repository.get_by_firebase_uid(firebase_uid)
        if user is None:
            raise UserNotFoundError()
        user_id = user.id

        # produces list of relationship entries where user_id is parent (or other)
        relationships = self.relationship_repository.get_children_per_user(user_id)

        # verify child_id has relationship with user_id
        matched_child_ids = {match.child_id for match in relationships}
        if child_id not in matched_child_ids:
            raise NoRelationshipFoundError()

        # fetch child data or error if N/A
        child = self.child_repository.get(child_id)
        if child is None:
            raise ChildNotFoundError()

        return ChildResponse.from_domain(child)

    def update_child(self,
        child_id: str,
        request: UpdateChild,
        firebase_uid: str
    ):
        pass
    

    # <--- HELPER FUNCTIONS --->
    def _get_linked_children(self, user_id: str):
        # ----->assumes existence of relationship_repo w/ get_children_per_user method
        # produces list of relationship entries where user_id is parent (or other)
        relationships = self.relationship_repository.get_children_per_user(user_id)
        # pull out child IDs from those relationships
        child_ids = [match.child_id for match in relationships]
        # return list of child entries from child repo where IDs match
        return self.child_repository.get_by_ids(child_ids)


