from flask import Blueprint, request
from app.services.content_service import ContentService
from app.utils.response import success_response

pronunciation_bp = Blueprint("pronunciation", __name__, url_prefix="/api/v1/pronunciation")


@pronunciation_bp.route("/words", methods=["GET"])
def list_words():
    """List pronunciation words with optional filters for level, category, pagination."""
    level = request.args.get("level", type=int)
    category = request.args.get("category", type=str)
    limit = request.args.get("limit", default=20, type=int)
    offset = request.args.get("offset", default=0, type=int)

    words = ContentService.get_pronunciation_words(
        level=level, category=category, limit=limit, offset=offset
    )
    return success_response(data=words, meta={"count": len(words), "limit": limit, "offset": offset})


@pronunciation_bp.route("/words/<string:word_id>", methods=["GET"])
def get_word(word_id: str):
    """Get full details of a specific pronunciation word item."""
    word = ContentService.get_pronunciation_word_by_id(word_id)
    return success_response(data=word)
