import logging
import sys


def setup_logger(app):
    """Configure structured logging for the Flask application."""
    log_level = logging.DEBUG if app.config.get("DEBUG") else logging.INFO
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] in %(module)s: %(message)s"
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)
    handler.setFormatter(formatter)

    app.logger.setLevel(log_level)
    if not app.logger.handlers:
        app.logger.addHandler(handler)

    return app.logger
