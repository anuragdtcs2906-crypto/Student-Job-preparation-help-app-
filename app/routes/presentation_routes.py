from flask import Blueprint, request
from app.services.content_service import ContentService
from app.utils.response import success_response

presentation_bp = Blueprint("presentations", __name__, url_prefix="/api/v1/presentations")


@presentation_bp.route("/tasks", methods=["GET"])
def list_tasks():
    """List presentation practice tasks with optional filters for level, category, pagination."""
    level = request.args.get("level", type=int)
    category = request.args.get("category", type=str)
    limit = request.args.get("limit", default=20, type=int)
    offset = request.args.get("offset", default=0, type=int)

    tasks = ContentService.get_presentation_tasks(
        level=level, category=category, limit=limit, offset=offset
    )
    return success_response(data=tasks, meta={"count": len(tasks), "limit": limit, "offset": offset})


@presentation_bp.route("/tasks/<string:task_id>", methods=["GET"])
def get_task(task_id: str):
    """Get full details of a specific presentation task."""
    task = ContentService.get_presentation_task_by_id(task_id)
    return success_response(data=task)
