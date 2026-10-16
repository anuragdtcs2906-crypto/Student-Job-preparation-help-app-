from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.recommendation.engine import RecommendationEngine
from app.utils.response import success_response

recommendation_bp = Blueprint("recommendations", __name__, url_prefix="/api/v1/recommendations")


@recommendation_bp.route("/<string:goal_slug>", methods=["GET"])
@jwt_required()
def get_recommendations(goal_slug: str):
    """
    Get personalized practice recommendations for a goal.
    Combines assessment result, current level, daily target, revision items, and difficulty history.
    """
    user_id = get_jwt_identity()
    limit = request.args.get("limit", default=None, type=int)
    recommendations = RecommendationEngine.generate_recommendations(
        user_id=user_id, goal_slug=goal_slug, limit_override=limit
    )
    return success_response(
        data=recommendations,
        meta={"count": len(recommendations), "goal_slug": goal_slug},
    )
