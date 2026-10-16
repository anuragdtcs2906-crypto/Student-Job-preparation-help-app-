from flask import Blueprint, request
from app.services.content_service import ContentService
from app.utils.response import success_response

interview_bp = Blueprint("interviews", __name__, url_prefix="/api/v1/interviews")


@interview_bp.route("/questions", methods=["GET"])
def list_questions():
    """List interview questions with optional filters for level, category, pagination."""
    level = request.args.get("level", type=int)
    category = request.args.get("category", type=str)
    limit = request.args.get("limit", default=20, type=int)
    offset = request.args.get("offset", default=0, type=int)

    questions = ContentService.get_interview_questions(
        level=level, category=category, limit=limit, offset=offset
    )
    return success_response(data=questions, meta={"count": len(questions), "limit": limit, "offset": offset})


@interview_bp.route("/questions/<string:question_id>", methods=["GET"])
def get_question(question_id: str):
    """Get full details of a specific interview question."""
    question = ContentService.get_interview_question_by_id(question_id)
    return success_response(data=question)
