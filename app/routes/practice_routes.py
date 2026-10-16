from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.practice_service import PracticeService
from app.repositories.goal_repository import GoalRepository
from app.repositories.practice_repository import PracticeRepository
from app.schemas.practice_schemas import (
    StartPracticeSessionRequest,
    SubmitPracticeAttemptRequest,
    CompletePracticeSessionRequest,
)
from app.utils.response import success_response
from app.utils.exceptions import NotFoundError

practice_bp = Blueprint("practice", __name__, url_prefix="/api/v1/practice")
practice_service = PracticeService()


@practice_bp.route("/sessions/start", methods=["POST"])
@jwt_required()
def start_practice_session():
    """Start a new practice session for a goal."""
    user_id = get_jwt_identity()
    payload = request.get_json() or {}
    validated = StartPracticeSessionRequest(**payload)

    session = practice_service.start_session(
        user_id=user_id,
        goal_slug=validated.goal_slug,
        activity_type=validated.activity_type,
        target_count=validated.target_count,
        session_metadata=validated.session_metadata,
    )
    return success_response(
        data=session,
        message="Practice session started.",
        status_code=201,
    )


@practice_bp.route("/attempts", methods=["POST"])
@jwt_required()
def submit_attempt():
    """Record an item practice attempt (word, question, task) with optional AI feedback."""
    user_id = get_jwt_identity()
    payload = request.get_json() or {}
    validated = SubmitPracticeAttemptRequest(**payload)

    attempt = practice_service.record_attempt(
        user_id=user_id,
        session_id=validated.session_id,
        content_type=validated.content_type,
        content_id=validated.content_id,
        user_input=validated.user_input,
        is_completed=validated.is_completed,
        marked_for_revision=validated.marked_for_revision,
        time_spent_seconds=validated.time_spent_seconds,
        request_ai_feedback=validated.request_ai_feedback,
    )
    return success_response(
        data=attempt,
        message="Practice attempt recorded.",
        status_code=200,
    )


@practice_bp.route("/sessions/<string:session_id>/complete", methods=["POST"])
@jwt_required()
def complete_practice_session(session_id: str):
    """Complete and close a practice session."""
    user_id = get_jwt_identity()
    payload = request.get_json() or {}
    duration = payload.get("duration_seconds")

    session = practice_service.complete_session(
        user_id=user_id,
        session_id=session_id,
        duration_seconds=duration,
    )
    return success_response(
        data=session,
        message="Practice session completed successfully.",
        status_code=200,
    )


@practice_bp.route("/sessions/active/<string:goal_slug>", methods=["GET"])
@jwt_required()
def get_active_session(goal_slug: str):
    """Get any ongoing active practice session for a goal."""
    user_id = get_jwt_identity()
    goal = GoalRepository.get_by_slug(goal_slug)
    if not goal:
        raise NotFoundError(f"Goal '{goal_slug}' not found.")

    active_sess = PracticeRepository.get_active_session(user_id, goal.id)
    if not active_sess:
        return success_response(data=None, message="No active session found.")
    return success_response(data=active_sess.to_dict(include_attempts=True))
