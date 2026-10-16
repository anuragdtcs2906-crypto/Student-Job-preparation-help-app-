from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.goal_service import GoalService
from app.services.level_service import LevelService
from app.services.target_service import TargetService
from app.schemas.goal_schemas import GoalSelectRequest, DailyTargetUpdateRequest
from app.utils.response import success_response

goal_bp = Blueprint("goals", __name__, url_prefix="/api/v1/goals")


@goal_bp.route("", methods=["GET"])
def list_goals():
    """List all available goals and their 5 configured levels."""
    goals = GoalService.get_all_goals()
    return success_response(data=goals)


@goal_bp.route("/<string:goal_slug>", methods=["GET"])
def get_goal_by_slug(goal_slug: str):
    """Get details of a specific goal."""
    goal = GoalService.get_goal_by_slug(goal_slug)
    return success_response(data=goal)


@goal_bp.route("/select", methods=["POST"])
@jwt_required()
def select_goals():
    """Select one or more goals to practice."""
    user_id = get_jwt_identity()
    payload = request.get_json() or {}
    validated = GoalSelectRequest(**payload)
    selected = GoalService.select_user_goals(user_id, validated.goal_slugs)
    return success_response(
        data=selected,
        message="Goals activated successfully.",
        status_code=200,
    )


@goal_bp.route("/my-goals", methods=["GET"])
@jwt_required()
def get_my_goals():
    """List goals selected by current user."""
    user_id = get_jwt_identity()
    user_goals = GoalService.get_user_goals(user_id)
    return success_response(data=user_goals)


@goal_bp.route("/<string:goal_slug>/levels", methods=["GET"])
def get_goal_levels(goal_slug: str):
    """List all 5 levels for a goal."""
    levels = LevelService.get_goal_levels(goal_slug)
    return success_response(data=levels)


@goal_bp.route("/<string:goal_slug>/levels/<int:level_number>", methods=["GET"])
def get_level_details(goal_slug: str, level_number: int):
    """Get details and mastery threshold for a specific level."""
    level = LevelService.get_level_details(goal_slug, level_number)
    return success_response(data=level)


@goal_bp.route("/<string:goal_slug>/progression-status", methods=["GET"])
@jwt_required()
def check_progression_status(goal_slug: str):
    """Check if the user is ready to attempt the next level progression check."""
    user_id = get_jwt_identity()
    status = LevelService.check_progression_eligibility(user_id, goal_slug)
    return success_response(data=status)


@goal_bp.route("/<string:goal_slug>/targets", methods=["PUT"])
@jwt_required()
def update_daily_target(goal_slug: str):
    """Set or update daily target quantity for a goal."""
    user_id = get_jwt_identity()
    payload = request.get_json() or {}
    validated = DailyTargetUpdateRequest(**payload)
    target = TargetService.update_daily_target(
        user_id=user_id,
        goal_slug=goal_slug,
        target_quantity=validated.target_quantity,
        target_type=validated.target_type,
    )
    return success_response(
        data=target,
        message=f"Daily target updated to {validated.target_quantity} items.",
    )
