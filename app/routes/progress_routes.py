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


@progress_bp.route("/heartbeat", methods=["POST"])
@jwt_required()
def record_heartbeat():
    """Record elapsed practice time from active sessions."""
    from flask import request
    user_id = get_jwt_identity()
    payload = request.get_json() or {}
    goal_slug = payload.get("goal_slug")
    seconds_spent = int(payload.get("seconds_spent", 0))
    result = ProgressService.record_heartbeat_time(user_id, goal_slug, seconds_spent)
    return success_response(data=result)


@progress_bp.route("/progress/<string:goal_slug>", methods=["GET"])
@jwt_required()
def get_goal_progress(goal_slug: str):
    """Fetch in-depth analytics, practice history, and calendar for a specific goal."""
    user_id = get_jwt_identity()
    details = ProgressService.get_goal_progress_details(user_id, goal_slug)
    return success_response(data=details)
