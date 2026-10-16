import pytest
from app.services.level_service import LevelService
from app.repositories.user_repository import UserRepository
from app.repositories.goal_repository import GoalRepository
from app.repositories.practice_repository import PracticeRepository
from app.utils.exceptions import NotFoundError


class TestLevelServiceUnit:
    def test_get_goal_levels(self, app):
        with app.app_context():
            levels = LevelService.get_goal_levels("interview")
            assert len(levels) == 5
            assert levels[0]["level_number"] == 1
            assert levels[4]["level_number"] == 5

    def test_get_goal_levels_not_found(self, app):
        with app.app_context():
            with pytest.raises(NotFoundError):
                LevelService.get_goal_levels("non-existent-goal")

    def test_get_level_details(self, app):
        with app.app_context():
            lvl = LevelService.get_level_details("pronunciation", 2)
            assert lvl["level_number"] == 2
            assert "configuration" in lvl
            assert lvl["configuration"]["assigned_level"] == 2

    def test_check_progression_eligibility(self, app):
        with app.app_context():
            user = UserRepository.create_anonymous_user()
            goal = GoalRepository.get_by_slug("communication")
            ug = UserRepository.get_or_create_user_goal(user.id, goal.id)

            # Initially 0 items completed -> not eligible
            status1 = LevelService.check_progression_eligibility(user.id, "communication")
            assert status1["eligible"] is False

            # After completing 3 items -> eligible
            prog = PracticeRepository.get_or_create_user_progress(user.id, goal.id)
            prog.total_items_completed = 3
            status2 = LevelService.check_progression_eligibility(user.id, "communication")
            assert status2["eligible"] is True

            # Max level 5
            ug.current_level = 5
            status3 = LevelService.check_progression_eligibility(user.id, "communication")
            assert status3["eligible"] is False
            assert status3["is_max_level"] is True
