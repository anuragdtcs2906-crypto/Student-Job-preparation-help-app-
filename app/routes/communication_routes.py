from flask import Blueprint, request
from app.services.content_service import ContentService
from app.utils.response import success_response

communication_bp = Blueprint("communication", __name__, url_prefix="/api/v1/communication")


@communication_bp.route("/exercises", methods=["GET"])
def list_exercises():
    """List Clear English communication exercises with optional filters for level, category, type."""
    level = request.args.get("level", type=int)
    category = request.args.get("category", type=str)
    exercise_type = request.args.get("type", type=str)
    limit = request.args.get("limit", default=20, type=int)
    offset = request.args.get("offset", default=0, type=int)

    exercises = ContentService.get_communication_exercises(
        level=level, category=category, exercise_type=exercise_type, limit=limit, offset=offset
    )
    return success_response(data=exercises, meta={"count": len(exercises), "limit": limit, "offset": offset})


@communication_bp.route("/exercises/<string:exercise_id>", methods=["GET"])
def get_exercise(exercise_id: str):
    """Get full details of a specific communication exercise."""
    exercise = ContentService.get_communication_exercise_by_id(exercise_id)
    return success_response(data=exercise)
