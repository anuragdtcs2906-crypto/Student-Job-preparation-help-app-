import os
from flask import Flask
from app.config import get_config, config_by_name
from app.extensions import db, jwt, cors, migrate
from app.routes import register_blueprints
from app.utils.error_handlers import register_error_handlers
from app.utils.logger import setup_logger


def create_app(config_name: str | None = None) -> Flask:
    """Application factory for AI Speaking & Communication Coach backend."""
    app = Flask(__name__)

    # Load configuration
    if config_name and config_name in config_by_name:
        app.config.from_object(config_by_name[config_name])
    else:
        app.config.from_object(get_config())

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config.get("CORS_ORIGINS", "*")}})
    migrate.init_app(app, db)

    # Logging & Error Handlers
    setup_logger(app)
    register_error_handlers(app)

    # Register API blueprints
    register_blueprints(app)

    @app.route("/", methods=["GET"])
    def root_index():
        from flask import request, render_template, jsonify
        
        # If client explicitly requests JSON, return API map
        if "application/json" in request.headers.get("Accept", "") and "text/html" not in request.headers.get("Accept", ""):
            return jsonify({
                "success": True,
                "service": "AI Personalized Speaking & Communication Coach API",
                "version": "1.0.0",
                "status": "online",
                "endpoints": {
                    "health": "/health",
                    "auth": "/api/v1/auth/anonymous",
                    "goals": "/api/v1/goals",
                    "pronunciation": "/api/v1/pronunciation/words",
                    "interview": "/api/v1/interviews/questions",
                    "presentation": "/api/v1/presentations/tasks",
                    "communication": "/api/v1/communication/exercises",
                    "gd": "/api/v1/gd/questions",
                    "assessments": "/api/v1/assessments/pronunciation/diagnostic",
                    "dashboard": "/api/v1/dashboard",
                },
            }), 200

        # Render the interactive frontend client
        return render_template("index.html")

    @app.route("/health", methods=["GET"])
    def health_check():
        return {
            "status": "healthy",
            "service": "AI Personalized Speaking & Communication Coach API",
            "version": "1.0.0",
        }, 200

    return app
