from flask import Flask
from app.routes.auth_routes import auth_bp
from app.routes.goal_routes import goal_bp
from app.routes.assessment_routes import assessment_bp
from app.routes.practice_routes import practice_bp
from app.routes.pronunciation_routes import pronunciation_bp
from app.routes.interview_routes import interview_bp
from app.routes.presentation_routes import presentation_bp
from app.routes.communication_routes import communication_bp
from app.routes.gd_routes import gd_bp
from app.routes.progress_routes import progress_bp
from app.routes.recommendation_routes import recommendation_bp
from app.routes.ai_routes import ai_bp


def register_blueprints(app: Flask) -> None:
    """Register all modular REST API blueprints."""
    app.register_blueprint(auth_bp)
    app.register_blueprint(goal_bp)
    app.register_blueprint(assessment_bp)
    app.register_blueprint(practice_bp)
    app.register_blueprint(pronunciation_bp)
    app.register_blueprint(interview_bp)
    app.register_blueprint(presentation_bp)
    app.register_blueprint(communication_bp)
    app.register_blueprint(gd_bp)
    app.register_blueprint(progress_bp)
    app.register_blueprint(recommendation_bp)
    app.register_blueprint(ai_bp)
