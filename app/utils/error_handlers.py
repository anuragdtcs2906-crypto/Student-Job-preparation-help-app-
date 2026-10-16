import logging
from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException
from pydantic import ValidationError as PydanticValidationError
from marshmallow import ValidationError as MarshmallowValidationError

from app.utils.exceptions import AppException
from app.utils.response import error_response

logger = logging.getLogger(__name__)


def register_error_handlers(app: Flask) -> None:
    """Register custom JSON error handlers for Flask."""

    @app.errorhandler(AppException)
    def handle_app_exception(exc: AppException):
        logger.warning(
            f"AppException [{exc.code}] on {request.method} {request.path}: {exc.message}"
        )
        return error_response(
            code=exc.code,
            message=exc.message,
            details=exc.details,
            status_code=exc.status_code,
        )

    @app.errorhandler(PydanticValidationError)
    def handle_pydantic_validation_error(exc: PydanticValidationError):
        logger.warning(f"Pydantic validation error on {request.method} {request.path}")
        sanitized_errors = []
        for err in exc.errors():
            sanitized_errors.append({
                "loc": [str(x) for x in err.get("loc", [])],
                "msg": str(err.get("msg", "")),
                "type": str(err.get("type", "")),
            })
        return error_response(
            code="VALIDATION_ERROR",
            message="Invalid request payload format.",
            details=sanitized_errors,
            status_code=400,
        )

    @app.errorhandler(MarshmallowValidationError)
    def handle_marshmallow_validation_error(exc: MarshmallowValidationError):
        logger.warning(f"Marshmallow validation error on {request.method} {request.path}")
        return error_response(
            code="VALIDATION_ERROR",
            message="Invalid input data.",
            details=exc.messages,
            status_code=400,
        )

    @app.errorhandler(HTTPException)
    def handle_http_exception(exc: HTTPException):
        logger.warning(
            f"HTTPException [{exc.code}] on {request.method} {request.path}: {exc.description}"
        )
        code_map = {
            400: "BAD_REQUEST",
            401: "UNAUTHORIZED",
            403: "FORBIDDEN",
            404: "NOT_FOUND",
            405: "METHOD_NOT_ALLOWED",
            422: "UNPROCESSABLE_ENTITY",
            429: "TOO_MANY_REQUESTS",
            500: "INTERNAL_SERVER_ERROR",
        }
        code = code_map.get(exc.code, "HTTP_ERROR")
        return error_response(
            code=code,
            message=exc.description or "HTTP error occurred.",
            status_code=exc.code or 500,
        )

    @app.errorhandler(Exception)
    def handle_unhandled_exception(exc: Exception):
        logger.exception(f"Unhandled exception on {request.method} {request.path}: {str(exc)}")
        return error_response(
            code="INTERNAL_SERVER_ERROR",
            message="An unexpected internal server error occurred. Please try again later.",
            status_code=500,
        )
