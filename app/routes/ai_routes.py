from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.ai.feedback_engine import AIFeedbackEngine
from app.repositories.goal_repository import GoalRepository
from app.repositories.user_repository import UserRepository
from app.schemas.ai_schemas import AIEvaluationRequest
from app.utils.response import success_response
from app.utils.exceptions import NotFoundError

ai_bp = Blueprint("ai", __name__, url_prefix="/api/v1/ai")
feedback_engine = AIFeedbackEngine()


@ai_bp.route("/evaluate", methods=["POST"])
@jwt_required()
def evaluate_open_ended_response():
    """
    Direct endpoint for evaluating open-ended interview answers, presentation scripts, or GD statements.
    Returns structured, supportive AI coaching feedback.
    """
    user_id = get_jwt_identity()
    payload = request.get_json() or {}
    validated = AIEvaluationRequest(**payload)

    goal = GoalRepository.get_by_slug(validated.goal_slug)
    if not goal:
        raise NotFoundError(f"Goal '{validated.goal_slug}' not found.")

    user_goal = UserRepository.get_user_goal_by_slug(user_id, validated.goal_slug)
    level = validated.level or (user_goal.current_level if user_goal else 1)

    result = feedback_engine.evaluate_response(
        user_id=user_id,
        goal_id=goal.id,
        goal_slug=validated.goal_slug,
        prompt_context=validated.prompt_context,
        user_response=validated.user_response,
        category=validated.category,
        level=level,
        source_type="direct_ai_evaluation",
        source_id="standalone_eval",
        save_to_db=False,
    )

    return success_response(
        data=result,
        message="AI feedback generated successfully.",
        status_code=200,
    )
