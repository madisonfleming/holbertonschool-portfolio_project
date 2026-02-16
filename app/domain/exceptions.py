# Just FYI the Exception is inbuilt Python base class, so we don't
# need to import to call exception and apply the message

# Child domain models
class InvalidChildNameError(Exception):
    def __init__(self, message="Child name must be provided"):
        super().__init__(message)

class InvalidDateOfBirthError(Exception):
    def __init__(self, message="Future birthdates are not accepted"):
        super().__init__(message)


# Milestone domain models
class InvalidMilestoneNameError(Exception):
    def __init__(self, message="Milestone name must be provided"):
        super().__init__(message)

class InvalidMilestoneDescriptionError(Exception):
    def __init__(self, message="Milestone description must be provided"):
        super().__init__(message)

class InvalidMilestoneThreshold(Exception):
    def __init__(self, message="Milestone threshold must be greater than 0"):
        super().__init__(message)

class InvalidMetricKeyError(Exception):
    def __init__(self, message="Metric key must be provided"):
        super().__init__(message)


# User domain models
class InvalidUserNameError(Exception):
    def __init__(self, message="User name must be provided"):
        super().__init__(message)

class InvalidEmailError(Exception):
    def __init__(self, message="Email must be provided"):
        super().__init__(message)


# Shared
# Called by facade but applies directly to domain models
class UserNotFoundError(Exception):
    def __init__(self, message="User not found"):
        super().__init__(message)

class ChildNotFoundError(Exception):
    def __init__(self, message="Child not found"):
        super().__init__(message)

