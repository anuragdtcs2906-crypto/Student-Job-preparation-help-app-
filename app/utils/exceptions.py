from typing import Any, Dict, Optional


class AppException(Exception):
    """Base exception for all application-specific errors."""

    status_code: int = 500
    code: str = "INTERNAL_SERVER_ERROR"

    def __init__(
        self,
        message: str = "An unexpected error occurred.",
        code: Optional[str] = None,
        status_code: Optional[int] = None,
        details: Optional[Any] = None,
    ):
        super().__init__(message)
        self.message = message
        if code:
            self.code = code
        if status_code:
            self.status_code = status_code
        self.details = details

    def to_dict(self) -> Dict[str, Any]:
        rv: Dict[str, Any] = {
            "code": self.code,
            "message": self.message,
        }
        if self.details is not None:
            rv["details"] = self.details
        return rv


class NotFoundError(AppException):
    status_code = 404
    code = "RESOURCE_NOT_FOUND"


class ValidationError(AppException):
    status_code = 400
    code = "VALIDATION_ERROR"


class AuthenticationError(AppException):
    status_code = 401
    code = "AUTHENTICATION_REQUIRED"


class ForbiddenError(AppException):
    status_code = 403
    code = "FORBIDDEN"


class ConflictError(AppException):
    status_code = 409
    code = "RESOURCE_CONFLICT"


class AssessmentError(AppException):
    status_code = 400
    code = "ASSESSMENT_ERROR"


class LevelProgressionError(AppException):
    status_code = 400
    code = "LEVEL_PROGRESSION_ERROR"


class AIServiceError(AppException):
    status_code = 502
    code = "AI_SERVICE_UNAVAILABLE"
