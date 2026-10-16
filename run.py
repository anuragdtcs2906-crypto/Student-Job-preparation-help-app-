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
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 5000))
    debug = app.config.get("DEBUG", True)
    
    print("\n" + "=" * 60)
    print(">> AI Personalized Speaking & Communication Coach")
    print(f">> Running locally at: http://localhost:{port}")
    print(f">> Direct IPv4 access: http://127.0.0.1:{port}")
    if host == "0.0.0.0":
        print(f">> Network access:    http://0.0.0.0:{port}")
    print("=" * 60 + "\n")

    app.run(host=host, port=port, debug=debug)
