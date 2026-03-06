#!/usr/bin/python3

from datetime import date, datetime, timedelta

from app.domain.user import User
from app.domain.child import Child
from app.domain.milestone import MilestoneType
from app.domain.milestone_completion import MilestoneCompletion

from app.persistence.user_repository import UserRepository
from app.persistence.child_repository import ChildRepository
from app.persistence.reading_session_repository import ReadingSessionRepository
from app.persistence.milestone_repository import MilestoneTypeRepository
from app.persistence.milestone_completion_repository import MilestoneCompletionRepository
from app.persistence.relationship_repository import RelationshipRepository #----->UPDATE this when join method completed
from app.persistence.book_repository import BookRepository

from app.external.open_library_api import OpenLibraryClient

#from app.api.schemas.users import CreateUser
from app.api.schemas.children import CreateChild, ChildResponse, UpdateChild
from app.api.schemas.users import CreateUser, UserResponse, UpdateUser
from app.api.schemas.reading_sessions import CreateReadingSession, UpdateReadingSession, ReadingSessionResponse
from app.api.schemas.books import BookResponse, BookSearchResponse
from app.api.schemas.milestones import CreateMilestone, MilestoneCompletionResponse

from app.domain.exceptions import(
    InvalidChildNameError,
    UserNotFoundError,
    ChildNotFoundError,
    InvalidUserNameError,
    InvalidEmailError,
    InvalidMilestoneNameError,
    InvalidMilestoneDescriptionError,
    InvalidMilestoneThresholdError,
    MilestoneNotFoundError,
)
from app.services.exceptions import(
    DuplicateUserError,
    InvalidSearchQueryError,
    BookNotFoundError,
    RelationshipNotFoundError,
    PermissionDeniedError,
    ReadingSessionNotFoundError
)


class MLBFacade:
    def __init__(
        self,
        user_repository: UserRepository,
        child_repository: ChildRepository,
        reading_session_repository: ReadingSessionRepository,
        milestone_repository: MilestoneTypeRepository,
        milestone_completion_repository: MilestoneCompletionRepository,
        relationship_repository: RelationshipRepository, #----->UPDATE this when join method completed
        book_repository: BookRepository,
        open_library_api: OpenLibraryClient
    ):
        self.user_repository = user_repository
        self.child_repository = child_repository
        self.reading_session_repository = reading_session_repository
        self.milestone_repository = milestone_repository
        self.milestone_completion_repository = milestone_completion_repository
        self.relationship_repository = relationship_repository #----->UPDATE this when join method completed
        self.book_repository = book_repository
        self.open_library_api = open_library_api

# <--- USER --->
    # Helper function to look up user by firebase_uid
    # Raises Permissions error if user doesn't exist
    # Can be called by any endpoint to authorise current user
    def get_user_id(
            self,
            firebase_uid,
    ):
        user = self.user_repository.get_by_firebase_uid(firebase_uid=firebase_uid)

        if user:
            return user.id
        
        raise PermissionDeniedError
        

# <--- CHILD --->
    
    def create_child(
        self,
        request: CreateChild,
        firebase_uid: str
    ):
        if not request.name.strip():    # validate request
            raise InvalidChildNameError()
        
        # create domain model
        child = Child(
            name=request.name,
            date_of_birth=request.date_of_birth,
            avatar_url=request.avatar_url
        )
        
        # save domain model to db
        self.child_repository.save(child)

        #placeholder logic to update the kid's avatar
        # self.child_repository.update_avatar(child.id, placeholder)

        
        # access user's ID via firebase ID
        user = self.user_repository.get_by_firebase_uid(firebase_uid)
        if user is None:
            raise UserNotFoundError()
        user_id = user.id

        # example creation of relationship join
        # ----->assumes existence of relationship_repo w/ add_member method
        self.relationship_repository.add_member(
            user_id=user_id,
            child_id=child.id,
            role="primary" # assuming parent default given they are creating child
        )

        # return ChildResponse.from_domain(self.child_repository.get(id))

        return ChildResponse.from_domain(child)   # convert domain model to response schema

    def get_children(self, firebase_uid: str):
        
        # access user's ID via firebase ID
        user = self.user_repository.get_by_firebase_uid(firebase_uid)
        if user is None:
            raise UserNotFoundError()
        user_id = user.id

        # produces list of relationship entries where user_id is parent (or other)
        relationships = self.relationship_repository.get_children_per_user(user_id) # NOTE: relationships gets user id + all owned child ids (list of dicts)
        if not relationships:
            return []
        
        # pull out child IDs from those relationships
        # child_ids = [match.child_id for match in relationships] # relationships is list of dicts (not objs) so .child_id doesn't exist yet
        child_ids = [match["child_id"] for match in relationships] # NOTE: child_ids gets list of child ids
        
        # fetch/retrieve linked children
        linked_children = self.child_repository.get_by_ids(child_ids) # NOTE: gets list of Child objects
        
        # doesn't throw error if children = 0, should allow empty Dashy
        return [ChildResponse.from_domain(child) for child in linked_children]

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
        relationships = self.relationship_repository.get_children_per_user(user_id) # NOTE: relationships gets user id + all owned child ids (list of dicts)
        
        # verify child_id has relationship with user_id
        # matched_child_ids = {match.child_id for match in relationships}
        matched_child_ids = {match["child_id"] for match in relationships} # NOTE: matched_child_ids gets a set of child_ids
        if child_id not in matched_child_ids:
            raise RelationshipNotFoundError(user_id, child_id)

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
        
        # access user's ID via firebase ID
        user = self.user_repository.get_by_firebase_uid(firebase_uid)
        if user is None:
            raise UserNotFoundError()
        user_id = user.id

        # produces list of relationship entries where user_id is parent (or other)
        relationships = self.relationship_repository.get_children_per_user(user_id) # NOTE: relationships gets user id + all owned child ids (list of dicts)

        # verify child_id has relationship with user_id
        # matched_child_ids = {match.child_id for match in relationships}
        matched_child_ids = {match["child_id"] for match in relationships} # NOTE: matched_child_ids gets a set of child_ids
        if child_id not in matched_child_ids:
            raise RelationshipNotFoundError()

        # fetch child data or error if N/A
        child = self.child_repository.get(child_id)
        if child is None:
            raise ChildNotFoundError()

        # apply updates with the fields provided by client
        if request.name is not None:
            child.name = request.name

        if request.date_of_birth is not None:
            child.date_of_birth = request.date_of_birth

        if request.avatar_url is not None:
            child.avatar_url = request.avatar_url

        # save updated child domain model to db
        self.child_repository.save(child)

        return ChildResponse.from_domain(child)

    # <--- USER --->
    # # DEV ONLY METHOD - DOESN'T SAVE TO REPO CORRECTLY (NO FB ID)
    # def create_user(
    #     self,
    #     request: CreateUser
    # ):
    #     if not request.name.strip():
    #         raise InvalidUserNameError()
    #     if not request.email.strip():
    #         raise InvalidEmailError()
       
    #     user = User(
    #         name=request.name,
    #         email=request.email,
    #     )
    #     self.user_repository.save(user)
    #     return UserResponse.from_domain(user)

    def get_user(
        self,
        firebase_uid
    ):
        # access user's ID via firebase ID
        user = self.user_repository.get_by_firebase_uid(firebase_uid)
        if user is None:
            raise UserNotFoundError()
        return UserResponse.from_domain(user)

    def update_user(
        self,
        request: UpdateUser,
        firebase_uid
    ):
        # access user's ID via firebase ID - error if None
        user = self.user_repository.get_by_firebase_uid(firebase_uid)
        if user is None:
            raise UserNotFoundError()

        # apply updates with the fields provided by client
        if request.name is not None:
            user.name = request.name
        # raise exception if email already exists in repo
        if request.email is not None:
            existing = self.user_repository.get_by_email(request.email)
            if existing and existing.id != user.id:
                raise DuplicateUserError()
            user.email = request.email

        # save updated user domain model to repo
        self.user_repository.save(user)
        return UserResponse.from_domain(user)

# <--- BOOKS --->

    # searches local & external dbs, returns list of books
    def search_books(
        self,
        q: str, # query
        subjects: list[str] | None = None, # TEST if this works for a single subject
        limit: int | None = None, # total results to be returned
    ):
        if not q or not q.strip():
            raise InvalidSearchQueryError()

        if limit is not None:
            if limit < 1:
                limit = None
            if limit > 40:
                limit = 40
            
        # take up to 30 results from our DB, then 30 from ext API, merge together
        local = self.book_repository.search(q, subjects, limit=30)
        external = self.open_library_api.search(q, subjects, limit=30)
        merged = local + external
        
        # ensure the merged list only contains unique books
        unique = {}
        for book in merged:
            unique[book.external_id] = book

        # return dict to a list of book values
        result = list(unique.values())

        # apply overall limit to result
        return result[:limit] if limit else result

    # searches local db only, using local book_id
    def get_book(
        self,
        book_id: str,
    ):
        book = self.book_repository.get(book_id)        
        if not book:
            raise BookNotFoundError(book_id) 
        
        return book
        

# <--- READING SESSIONS --->

    def create_reading_session(
        self,
        request: CreateReadingSession, # child_id, external_id
        firebase_uid: str,
    ):
    
        # access user's ID via firebase ID
        user = self.user_repository.get_by_firebase_uid(firebase_uid)
        if user is None:
            raise UserNotFoundError()
        user_id = user.id

        # validate child-user relationship
        child_id = request.child_id
        has_rel = self.relationship_repository.has_relationship(user_id, child_id)
        if not has_rel:
            raise RelationshipNotFoundError(user_id, child_id)

        # save book details to the DB if not existing
        book = self.book_repository.get_or_save(
            external_id=request.external_id,
            source="openlibrary",
            title=request.title,
            author=request.author,
            cover_url=request.cover_url
        )

        # create reading session
        session = self.reading_session_repository.save(
            child_id=child_id,
            book_id=book.id,
            logged_at=request.logged_at
        )

        # check if a "books_read" milestone has been achieved
        current_total = self.count_reading_sessions(child_id, firebase_uid)

        # create milestone record at defined intervals of total # of books read
        if current_total == 25 or current_total % 50 == 0:
            milestone = self.milestone_repository.get_by_type_and_threshold(milestone_type="books_read", threshold=current_total)
            self.create_milestone_record(child_id, milestone, completed_at=request.logged_at)
        

        return ReadingSessionResponse.from_domain(session)


    def get_reading_sessions(
        self,
        child_id: int,
        firebase_uid: str,
        limit: int | None = None,
        from_date: date | None = None,
        to_date: date | None = None,
    ):
        # access user's ID via firebase ID
        user = self.user_repository.get_by_firebase_uid(firebase_uid)
        if user is None:
            raise UserNotFoundError()
        user_id = user.id

        # validate child-user relationship
        allowed_session_roles = ["primary", "secondary"]
        has_acc = self.relationship_repository.has_one_of_roles(user_id, child_id, allowed_session_roles)
        if not has_acc:
            raise PermissionDeniedError()

        # retrieve sessions from db
        sessions = self.reading_session_repository.get_by_child(child_id)

        # apply date filters
        filtered_sessions = []

        for session in sessions:
            session_date = session.logged_at.date()

            if from_date is not None and session_date < from_date:
                continue
            if to_date is not None and session_date > to_date:
                continue
            filtered_sessions.append(session)

        # sort results from most recent entry
        filtered_sessions.sort(key=lambda session: session.logged_at, reverse=True)

        if limit is not None:
            filtered_sessions = filtered_sessions[:limit]

        return [ReadingSessionResponse.from_domain(session) for session in filtered_sessions]


    def update_session(
        self,
        session_id: str,
        updated: UpdateReadingSession,
        firebase_uid: str,
    ):
        # access user's ID via firebase ID
        user = self.user_repository.get_by_firebase_uid(firebase_uid)
        if user is None:
            raise UserNotFoundError()
        user_id = user.id

        # retrieve existing session
        session = self.reading_session_repository.get_by_id(session_id)
        if session is None:
            raise ReadingSessionNotFoundError(session_id)

        # validate child-user relationship
        allowed_session_roles = ["primary", "secondary"]
        has_acc = self.relationship_repository.has_one_of_roles(
            user_id,
            session.child_id,
            allowed_session_roles
        )
        if not has_acc:
            raise PermissionDeniedError()

        # update
        if updated.book_id is not None:
            session.book_id = updated.book_id
        if updated.logged_at is not None:
            session.logged_at = updated.logged_at

        self.reading_session_repository.update(session)

        return ReadingSessionResponse.from_domain(session)


    # return number of sessions in a date window
    # return all sessions ever recorded
    def count_reading_sessions(
        self,
        child_id: int,
        firebase_uid: str,
        from_date: date | None = None,
        to_date: date | None = None,
    ):
        # access user's ID via firebase ID
        user = self.user_repository.get_by_firebase_uid(firebase_uid)
        if user is None:
            raise UserNotFoundError()
        user_id = user.id

        # validate child-user relationship
        allowed_session_roles = ["primary", "secondary"]
        has_acc = self.relationship_repository.has_one_of_roles(
            user_id,
            child_id,
            allowed_session_roles
        )
        if not has_acc:
            raise PermissionDeniedError()

        # retrieve sessions by child_id
        sessions = self.reading_session_repository.get_by_child(child_id)

        # apply date filters
        count = 0
        for session in sessions:
            session_date = session.logged_at.date()

            if from_date is not None and session_date < from_date:
                continue
            if to_date is not None and session_date > to_date:
                continue
            count += 1

        return count

    def heatmap_count_rs(
        self,
        child_id: int,
        firebase_uid: str,
        from_date: date | None = None,
        to_date: date | None = None,
    ):
        # access user's ID via firebase ID
        user = self.user_repository.get_by_firebase_uid(firebase_uid)
        if user is None:
            raise UserNotFoundError()
        user_id = user.id

        # validate child-user relationship
        allowed_session_roles = ["primary", "secondary"]
        has_acc = self.relationship_repository.has_one_of_roles(
            user_id,
            child_id,
            allowed_session_roles
        )
        if not has_acc:
            raise PermissionDeniedError()

        # retrieve sessions by child_id
        sessions = self.reading_session_repository.get_by_child(child_id)

        # group sessions by date and build counts
        counts: dict[date, int] = {}

        for session in sessions:
            session_date = session.logged_at.date()

            if from_date is not None and session_date < from_date:
                continue
            if to_date is not None and session_date > to_date:
                continue

            counts[session_date] = counts.get(session_date, 0) + 1

        # enter a 0 for missing days
        if from_date and to_date:
            current = from_date
            while current <= to_date:
                counts.setdefault(current, 0)
                current += timedelta(days=1)    # timedelta detects duration (increments by 1 day)

        return counts

# <--- MILESTONES --->

    def get_milestones(self, child_id: str, firebase_uid: str) -> list[MilestoneCompletionResponse]:
        user = self.user_repository.get_by_firebase_uid(firebase_uid)
        user_id = user.id
        # validate child-user relationship
        if user_id:
            has_rel = self.relationship_repository.has_relationship(user_id, child_id)
            if not has_rel:
                raise RelationshipNotFoundError(user_id, child_id)

        milestones = self.milestone_completion_repository.get_all_milestones_by_child(child_id)
        return milestones
    
    def get_milestone(self, child_id: str, milestone_id: str, firebase_uid: str) -> MilestoneCompletionResponse:
        
        user = self.user_repository.get_by_firebase_uid(firebase_uid)
        user_id = user.id
        # validate child-user relationship
        if user_id:
            has_rel = self.relationship_repository.has_relationship(user_id, child_id)
            if not has_rel:
                raise RelationshipNotFoundError(user_id, child_id)
            
        if not milestone_id:
            raise MilestoneNotFoundError()

        milestone = self.milestone_completion_repository.get(milestone_id=milestone_id)

        if milestone is None:
            raise MilestoneNotFoundError

        return milestone

    def get_milestones_by_type(self, child_id, type, firebase_uid) -> MilestoneCompletionResponse:
        user = self.user_repository.get_by_firebase_uid(firebase_uid)
        user_id = user.id
        # validate child-user relationship
        if user_id:
            has_rel = self.relationship_repository.has_relationship(user_id, child_id)
            if not has_rel:
                raise RelationshipNotFoundError(user_id, child_id)
        
        # TO DO - validate type against a known list, raise applicable error
        if not type:
            raise ValueError("Missing milestone type")

        milestone = self.milestone_completion_repository.get_all_by_child_and_key(child_id, type)
        return milestone

    def create_weekly_milestone(self, milestone_request: CreateMilestone, firebase_uid):
        user_id = self.get_user_id(firebase_uid)

        # validate child-user relationship
        if user_id:
            child_id = milestone_request.child_id  # Check syntax
            has_rel = self.relationship_repository.has_relationship(user_id, child_id)
            if not has_rel:
                raise RelationshipNotFoundError(user_id, child_id)
        
        # validate child exists
        child = self.child_repository.get(child_id)

        # find milestone by subject included on request
        # if child and milestone_request["subject"]:
        if child:
            # To do - Ensure that subject is one of the valid options
            milestone = self.milestone_repository.get_by_subject(milestone_request.subject)
            milestone_record = self.create_milestone_record(
                milestone_request.child_id,
                milestone,
                completed_at=datetime.utcnow()
            )
            return milestone_record.to_dict()
            # return milestone_record


    def create_milestone_record(
        self,
        child_id: str,
        milestone: dict,
        completed_at: datetime):
        """
        Creates either a total milestone record or a weekly milestone record
        """
        child = self.child_repository.get(child_id)
        if not child:
            raise ChildNotFoundError
        if not milestone:
            raise MilestoneNotFoundError

        if milestone["type"] == "books_read":
            name = milestone["name"]
            percentage = milestone["threshold"] / 1000
            description = f'{child.name} has read {milestone["threshold"]} books! That\'s {percentage}% of the total goal!'

        elif milestone["type"] == "weekly_goal":
            name = milestone["name"]
            description = f'{child.name} read {milestone["threshold"]} books about {milestone["subject"]} this week!'

        else:
            name = milestone["name"]
            description = ""

        # create a Milestone object
        milestone_record = MilestoneCompletion(
            child_id=child_id,
            milestone_id=milestone["id"],
            description=description,
            completed_at=completed_at,
        )
        self.milestone_completion_repository.save(milestone_record)

        return {
            **milestone_record.to_dict(),
            "name": name,
            "description": description,
            "threshold": milestone["threshold"],
            "subject": milestone.get("subject"),
            "type": milestone["type"],
        }