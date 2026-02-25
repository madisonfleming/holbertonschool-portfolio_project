from app.persistence.book_repository import BookRepository
from app.persistence.reading_session_repository import ReadingSessionRepository
from app.external.open_library_api import OpenLibraryClient

from app.api.schemas.books import BookResponse, BookSearchResponse
from app.api.schemas.reading_sessions import CreateReadingSession

from app.services.exceptions import InvalidSearchQueryError

from datetime import date

class MLBFacade:
    def __init__(
        self,
        book_repository: BookRepository,
        reading_session_repository: ReadingSessionRepository,
        open_library_api: OpenLibraryClient
    ):
        self.book_repository = book_repository
        self.reading_session_repository = reading_session_repository
        self.open_library_api = open_library_api

# <--- BOOKS --->

    def search_books(
        self,
        q: str, # query
        # firebase_uid: str,
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


    def get_book(self, book_id, firebase_uid):
        pass

    # <--- READING SESSIONS --->

    def create_reading_session(
        self,
        request: CreateReadingSession,
        firebase_uid: str
    ):
        pass
    # validate user (firebase_uid)
    # validate child-user relationship
    # upsert book into DB
    # create reading session
    # return session response



    # include optional limit=# so they can pull {number} of results as required
    # this facilitates get_last_session method because they can set limit to 1
    def get_reading_sessions(child_id: int, limit: int | None = None):
        sessions = reading_session_repository.get_sessions(child_id)

        if limit is not None:
            sessions = sessions[:limit]

        return sessions
        """
        - sorts by logged_at DESC
        - accepts an optional limit
        - returns the sessions in that order
        """

    def update_session():
        pass

    # to facilitate heatmap function for fronties
    # return number of sessions in a date window
    # return all sessions ever recorded
    def count_reading_sessions():
        """
        - fetch sessions
        - group by date
        - count
        - fill missing days
        - return clean structure
        """