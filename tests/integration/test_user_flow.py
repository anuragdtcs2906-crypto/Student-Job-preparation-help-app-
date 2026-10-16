import pytest
from app.services.auth_service import AuthService
from app.services.goal_service import GoalService
from app.repositories.user_repository import UserRepository


class TestUserFlow:
    def test_anonymous_registration_and_login(self, app):
        with app.app_context():
            # 1. Register new anonymous user
            reg_result = AuthService.register_anonymous_user()
            anon_id = reg_result["anonymous_id"]
            token = reg_result["access_token"]
            assert len(anon_id) == 8
            assert token is not None

            # 2. Login with existing anonymous ID
            login_result = AuthService.login_anonymous_user(anon_id)
            assert login_result["anonymous_id"] == anon_id
            assert login_result["access_token"] is not None

            # 3. Fetch profile
            user = UserRepository.get_by_anonymous_id(anon_id)
            profile = AuthService.get_current_user_profile(user.id)
            assert profile["anonymous_id"] == anon_id

    def test_multi_goal_selection(self, app):
        with app.app_context():
            user = UserRepository.create_anonymous_user()
            selected = GoalService.select_user_goals(user.id, ["pronunciation", "interview", "presentation"])

            assert len(selected) == 3
            user_goals = GoalService.get_user_goals(user.id)
            slugs = {ug["goal_slug"] for ug in user_goals}
            assert slugs == {"pronunciation", "interview", "presentation"}
