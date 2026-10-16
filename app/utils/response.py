from typing import Any, Dict, Optional, Tuple
from flask import jsonify, Response


def success_response(
    data: Any = None,
    message: Optional[str] = None,
    meta: Optional[Dict[str, Any]] = None,
    status_code: int = 200,
) -> Tuple[Response, int]:
    """Generate a standardized JSON success response."""
    payload: Dict[str, Any] = {"success": True}
    if data is not None:
        payload["data"] = data
    if message is not None:
        payload["message"] = message
    if meta is not None:
        payload["meta"] = meta
    return jsonify(payload), status_code


def error_response(
    code: str,
    message: str,
    details: Any = None,
    status_code: int = 400,
) -> Tuple[Response, int]:
    """Generate a standardized JSON error response."""
    error_payload: Dict[str, Any] = {
        "code": code,
        "message": message,
    }
    if details is not None:
        error_payload["details"] = details

    payload: Dict[str, Any] = {
        "success": False,
        "error": error_payload,
    }
    return jsonify(payload), status_code
