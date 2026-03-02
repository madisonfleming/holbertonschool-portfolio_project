# Just FYI the Exception is inbuilt Python base class, so we don't
# need to import to call exception and apply the message

class DuplicateUserError(Exception):
    def __init__(self, message="User already exists"):
        super().__init__(message)

class RelationshipNotFoundError(Exception):
    def __init__(self, user_id, child_id):
        message = f"Relationship between user: '{user_id}' and child: '{child_id}' not found"
        super().__init__(message)

class ExternalBookClientError(Exception):
    def __init__(self, message="Open Library is currently unavailable"):
        super().__init__(message)

class InvalidSearchQueryError(Exception):
    def __init__(self, message="Search field cannot be empty"):
        super().__init__(message)

class BookNotFoundError(Exception):
    def __init__(self, book_id: str):
        message = f"Book with id: '{book_id}' not found"
        super().__init__(message)

class PermissionDeniedError(Exception):
    def __init__(self, message="Insufficient permissions to complete this action"):
        super().__init__(message)

class ReadingSessionNotFoundError(Exception):
    def __init__(self, session_id: str):
        message = f"Reading session with id: '{session_id}' not found"
        super().__init__(message)