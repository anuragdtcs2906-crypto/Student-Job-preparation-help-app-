from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.progress_service import ProgressService
from app.utils.response import success_response

progress_bp = Blueprint("progress", __name__, url_prefix="/api/v1")


@progress_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def get_dashboard():
    """Fetch complete personalized dashboard across all active goals."""
    user_id = get_jwt_identity()
    summary = ProgressService.get_dashboard_summary(user_id)
    return success_response(data=summary)


@progress_bp.route("/progress/<string:goal_slug>", methods=["GET"])
@jwt_required()
def get_goal_progress(goal_slug: str):
    """Fetch in-depth analytics, practice history, and calendar for a specific goal."""
    user_id = get_jwt_identity()
    details = ProgressService.get_goal_progress_details(user_id, goal_slug)
    return success_response(data=details)
