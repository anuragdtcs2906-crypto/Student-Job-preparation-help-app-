import os
from app import create_app
from app.extensions import db
from seed.seed_runner import run_all_seeds

app = create_app()

with app.app_context():
    # Automatically initialize tables and seed default data if database is empty
    db.create_all()
    try:
        from app.models.goal import Goal
        if not Goal.query.first():
            run_all_seeds()
    except Exception as e:
        app.logger.warning(f"Seed check: {e}")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=app.config.get("DEBUG", True))
