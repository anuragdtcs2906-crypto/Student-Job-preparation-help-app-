from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.assessment_service import AssessmentService
from app.repositories.assessment_repository import AssessmentRepository
from app.repositories.goal_repository import GoalRepository
from app.schemas.assessment_schemas import AssessmentSubmissionRequest
from app.utils.response import success_response
from app.utils.exceptions import NotFoundError

assessment_bp = Blueprint("assessments", __name__, url_prefix="/api/v1/assessments")
assessment_service = AssessmentService()


@assessment_bp.route("/<string:goal_slug>/diagnostic", methods=["GET"])
def get_diagnostic_assessment(goal_slug: str):
    """Fetch initial diagnostic assessment questions for a goal."""
    assessment = assessment_service.get_diagnostic_assessment(goal_slug)
    return success_response(data=assessment)


@assessment_bp.route("/<string:goal_slug>/progression/<int:level_number>", methods=["GET"])
def get_progression_assessment(goal_slug: str, level_number: int):
    """Fetch level progression assessment questions."""
    assessment = assessment_service.get_progression_assessment(goal_slug, level_number)
    return success_response(data=assessment)


@assessment_bp.route("/<string:goal_slug>/submit", methods=["POST"])
@jwt_required()
def submit_assessment(goal_slug: str):
    """Submit diagnostic or progression assessment answers."""
    user_id = get_jwt_identity()
    payload = request.get_json() or {}
    validated = AssessmentSubmissionRequest(**payload)

    result = assessment_service.submit_assessment(
        user_id=user_id,
        goal_slug=goal_slug,
        assessment_id=validated.assessment_id,
        answers_payload=[a.model_dump() for a in validated.answers],
    )
    return success_response(
        data=result,
        message="Assessment evaluated successfully.",
        status_code=200,
    )


@assessment_bp.route("/<string:goal_slug>/history", methods=["GET"])
@jwt_required()
def get_assessment_history(goal_slug: str):
    """Get history of assessments completed for this goal."""
    user_id = get_jwt_identity()
    goal = GoalRepository.get_by_slug(goal_slug)
    if not goal:
        raise NotFoundError(f"Goal '{goal_slug}' not found.")

    attempts = AssessmentRepository.get_attempts_for_user(user_id, goal.id)
    return success_response(data=[att.to_dict(include_answers=True) for att in attempts])
