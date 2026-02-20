# Just FYI the Exception is inbuilt Python base class, so we don't
# need to import to call exception and apply the message

class DuplicateUserError(Exception):
    def __init__(self, message="User already exists"):
        super().__init__(message)

class RelationshipNotFoundError(Exception):
    def __init__(self, message="Relationship not found"):
        super().__init__(message)
