from flask import Blueprint, request
from app.services.content_service import ContentService
from app.utils.response import success_response

gd_bp = Blueprint("gd", __name__, url_prefix="/api/v1/gd")


@gd_bp.route("/questions", methods=["GET"])
def list_gd_questions():
    """List Group Discussion and workplace communication scenarios."""
    level = request.args.get("level", type=int)
    category = request.args.get("category", type=str)
    limit = request.args.get("limit", default=20, type=int)
    offset = request.args.get("offset", default=0, type=int)

    questions = ContentService.get_gd_questions(
        level=level, category=category, limit=limit, offset=offset
    )
    return success_response(data=questions, meta={"count": len(questions), "limit": limit, "offset": offset})


@gd_bp.route("/questions/<string:gd_id>", methods=["GET"])
def get_gd_question(gd_id: str):
    """Get full details of a specific GD scenario."""
    gd = ContentService.get_gd_question_by_id(gd_id)
    return success_response(data=gd)
