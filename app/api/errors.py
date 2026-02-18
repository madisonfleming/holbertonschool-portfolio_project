# register all app and domain-level exception handlers
# these convert internal exceptions into JSON API responses

import logging
from pydantic import BaseModel

from fastapi.responses import JSONResponse
from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from app.domain.exceptions import (
    InvalidChildNameError,
    InvalidDateOfBirthError,
    InvalidMilestoneNameError,
    InvalidMilestoneDescriptionError,
    InvalidMilestoneThresholdError,
    InvalidMetricKeyError,
    InvalidUserNameError,
    InvalidEmailError,
    UserNotFoundError,
    ChildNotFoundError
)
from app.services.exceptions import (
    DuplicateUserError,
    RelationshipNotFoundError
)

def format_error(code: str, exc: Exception, status: int):
    # helper function to prevent repetition
    return JSONResponse(
        status_code=status,
        content={
            "error": code,
            "message": str(exc),
            "status": status
        }
    )

def register_error_handlers(app):
    logging.info("Registering error handlers...")

    @app.exception_handler(HTTPException)
    # this handles any of FastAPI's HTTPExceptions raised manually in the app
    async def http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.detail,
                "message": exc.detail,
                "status": exc.status_code
            }
        )

    @app.exception_handler(RequestValidationError)
    # gives JSON shape to FastAPI inbuilt exception
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return format_error("VALIDATION_ERROR", exc, 400)

    @app.exception_handler(DuplicateUserError)
    async def duplicate_user_handler(request: Request, exc: DuplicateUserError):
        return format_error("USER_ALREADY_EXISTS", exc, 409)

    @app.exception_handler(UserNotFoundError)
    async def user_not_found_handler(request: Request, exc: UserNotFoundError):
        return format_error("USER_NOT_FOUND", exc, 404)

    @app.exception_handler(ChildNotFoundError)
    async def child_not_found_handler(request: Request, exc: ChildNotFoundError):
        return format_error( "CHILD_NOT_FOUND", exc, 404)

    @app.exception_handler(InvalidUserNameError)
    async def invalid_name_handler(request: Request, exc: InvalidUserNameError):
        return format_error("INVALID_USER_NAME", exc, 400)

    @app.exception_handler(InvalidEmailError)
    async def invalid_email_handler(request: Request, exc: InvalidEmailError):
        return format_error("INVALID_EMAIL", exc, 400)

    @app.exception_handler(InvalidMilestoneNameError)
    async def invalid_milestone_name_handler(request: Request, exc: InvalidMilestoneNameError):
        return format_error("INVALID_MILESTONE_NAME", exc, 400)

    @app.exception_handler(InvalidMilestoneDescriptionError)
    async def invalid_milestone_description_handler(request: Request, exc: InvalidMilestoneDescriptionError):
        return format_error("INVALID_MILESTONE_DESCRIPTION", exc, 400)

    @app.exception_handler(InvalidMilestoneThresholdError)
    async def invalid_milestone_threshold(request: Request, exc: InvalidMilestoneThresholdError):
        return format_error("INVALID_MILESTONE_THRESHOLD", exc, 400)

    @app.exception_handler(InvalidMetricKeyError)
    async def invalid_metric_key_handler(request: Request, exc: InvalidMetricKeyError):
        return format_error("INVALID_METRIC_KEY", exc, 400)

    @app.exception_handler(InvalidChildNameError)
    async def invalid_child_name_handler(request: Request, exc: InvalidChildNameError):
        return format_error("INVALID_CHILD_NAME", exc, 400)

    @app.exception_handler(InvalidDateOfBirthError)
    async def invalid_date_of_birth_handler(request: Request, exc: InvalidDateOfBirthError):
        return format_error("INVALID_DATE_OF_BIRTH", exc, 400)

    @app.exception_handler(RelationshipNotFoundError)
    async def relationship_not_found_handler(request: Request, exc: RelationshipNotFoundError):
        return format_error("RELATIONSHIP_NOT_FOUND", exc, 400)