from typing import Dict, Any, Tuple
from flask_jwt_extended import create_access_token
from app.repositories.user_repository import UserRepository
from app.utils.exceptions import NotFoundError, ValidationError
from app.utils.anonymous_id import validate_anonymous_id, normalize_anonymous_id


class AuthService:
    """Service handling anonymous registration and session access."""

    @staticmethod
    def register_anonymous_user() -> Dict[str, Any]:
        """Generate a brand new anonymous account and return token."""
        user = UserRepository.create_anonymous_user()
        access_token = create_access_token(identity=user.id, additional_claims={"anonymous_id": user.anonymous_id})
        return {
            "anonymous_id": user.anonymous_id,
            "access_token": access_token,
            "token_type": "Bearer",
            "created_at": user.created_at.isoformat() if user.created_at else None,
        }

    @staticmethod
    def login_anonymous_user(anonymous_id: str) -> Dict[str, Any]:
        """Authenticate an existing user using their 8-character anonymous ID."""
        normalized = normalize_anonymous_id(anonymous_id)
        if not validate_anonymous_id(normalized):
            raise ValidationError("Invalid anonymous ID format. Please verify your 8-character ID.")

        user = UserRepository.get_by_anonymous_id(normalized)
        if not user:
            raise NotFoundError("Anonymous ID not found. Please check your ID or create a new account.")

        UserRepository.update_last_active(user)
        access_token = create_access_token(identity=user.id, additional_claims={"anonymous_id": user.anonymous_id})

        return {
            "anonymous_id": user.anonymous_id,
            "access_token": access_token,
            "token_type": "Bearer",
            "goals_count": len(user.user_goals),
            "last_active_at": user.last_active_at.isoformat() if user.last_active_at else None,
        }

    @staticmethod
    def get_current_user_profile(user_id: str) -> Dict[str, Any]:
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found.")

        UserRepository.update_last_active(user)
        return {
            "anonymous_id": user.anonymous_id,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "last_active_at": user.last_active_at.isoformat() if user.last_active_at else None,
            "goals": [ug.to_dict() for ug in user.user_goals if ug.is_active],
            "daily_targets": [dt.to_dict() for dt in user.daily_targets if dt.is_active],
        }
