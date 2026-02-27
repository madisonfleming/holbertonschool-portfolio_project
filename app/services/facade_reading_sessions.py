from app.persistence.book_repository import BookRepository
from app.persistence.reading_session_repository import ReadingSessionRepository
from app.external.open_library_api import OpenLibraryClient

from app.api.schemas.books import BookResponse, BookSearchResponse
from app.api.schemas.reading_sessions import (
    CreateReadingSession,
    UpdateReadingSession,
    ReadingSessionResponse
)

from app.domain.exceptions import UserNotFoundError

from app.services.exceptions import (
    InvalidSearchQueryError,
    BookNotFoundError,
    RelationshipNotFoundError,
    PermissionDeniedError,
    ReadingSessionNotFoundError
)


from datetime import date, timedelta

class MLBFacade:
    def __init__(
        self,
        book_repository: BookRepository,
        reading_session_repository: ReadingSessionRepository,
        open_library_api: OpenLibraryClient
        user_repository: UserRepository
        relationship_repository: RelationshipRepository
    ):
        self.book_repository = book_repository
        self.reading_session_repository = reading_session_repository
        self.open_library_api = open_library_api
        self.user_repository = user_repository
        self.relationship_repository = relationship_repository


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
        firebase_uid: str
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

        # check if a milestone has been achieved TODO FINISH THIS GUYYYY
        # I'm thinking that milestones per child will be calculated in the
        # facade directly:
        #    self._evaluate_milestones(child_id, session)

        return ReadingSessionResponse.from_domain(session)


    def get_reading_sessions(
        self,
        child_id: int,
        limit: int | None = None,
        from_date: date | None = None,
        to_date: date | None = None,
        firebase_uid: str
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

        return filtered_sessions


    def update_session(
        self,
        session_id: str,
        updated: UpdateReadingSession,
        firebase_uid: str
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

        return session


    # return number of sessions in a date window
    # return all sessions ever recorded
    def count_reading_sessions(
        self,
        child_id: int,
        from_date: date | None = None,
        to_date: date | None = None,
        firebase_uid: str
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
        from_date: date | None = None,
        to_date: date | None = None,
        firebase_uid: str
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
