import os
import sys

# Add root project folder to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from app import create_app
from app.extensions import db as _db
from seed.seed_runner import run_all_seeds
from app.repositories.user_repository import UserRepository
from flask_jwt_extended import create_access_token


@pytest.fixture(scope="session")
def app():
    """Session-wide test Flask application."""
    test_app = create_app("testing")
    with test_app.app_context():
        _db.create_all()
        run_all_seeds()
        yield test_app
        _db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    """A test client for making HTTP requests."""
    return app.test_client()


@pytest.fixture(scope="function")
def runner(app):
    """A test runner for CLI commands."""
    return app.test_cli_runner()


@pytest.fixture(scope="function")
def db_session(app):
    """Database session fixture with rollback per test."""
    with app.app_context():
        yield _db.session
        _db.session.rollback()


@pytest.fixture(scope="function")
def test_user(app):
    """Create a clean anonymous test user."""
    with app.app_context():
        user = UserRepository.create_anonymous_user()
        token = create_access_token(identity=user.id, additional_claims={"anonymous_id": user.anonymous_id})
        return {
            "id": user.id,
            "anonymous_id": user.anonymous_id,
            "token": token,
            "headers": {"Authorization": f"Bearer {token}"},
        }
