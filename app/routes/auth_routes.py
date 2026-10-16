from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.auth_service import AuthService
from app.schemas.auth_schemas import AnonymousAuthRequest
from app.utils.response import success_response

auth_bp = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth_bp.route("/anonymous", methods=["POST"])
def register_anonymous():
    """Create a new unique anonymous user account."""
    result = AuthService.register_anonymous_user()
    return success_response(
        data=result,
        message="Anonymous account created successfully. Keep your anonymous ID to access your progress.",
        status_code=201,
    )


@auth_bp.route("/login", methods=["POST"])
def login_anonymous():
    """Authenticate with an existing anonymous ID."""
    payload = request.get_json() or {}
    validated = AnonymousAuthRequest(**payload)
    result = AuthService.login_anonymous_user(validated.anonymous_id)
    return success_response(
        data=result,
        message="Welcome back! Session authenticated successfully.",
        status_code=200,
    )


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    """Fetch current authenticated user profile."""
    user_id = get_jwt_identity()
    profile = AuthService.get_current_user_profile(user_id)
    return success_response(data=profile)
