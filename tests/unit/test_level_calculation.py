import pytest
from app.repositories.goal_repository import GoalRepository


class TestLevelCalculation:
    def test_deterministic_level_mapping(self, app):
        with app.app_context():
            goal = GoalRepository.get_by_slug("pronunciation")
            assert goal is not None

            # Score thresholds:
            # 0% - 29.9% -> Level 1
            # 30% - 49.9% -> Level 2
            # 50% - 69.9% -> Level 3
            # 70% - 84.9% -> Level 4
            # 85% - 100%  -> Level 5

            assert GoalRepository.match_level_from_score(goal.id, 0.0) == 1
            assert GoalRepository.match_level_from_score(goal.id, 25.0) == 1
            assert GoalRepository.match_level_from_score(goal.id, 30.0) == 2
            assert GoalRepository.match_level_from_score(goal.id, 45.0) == 2
            assert GoalRepository.match_level_from_score(goal.id, 50.0) == 3
            assert GoalRepository.match_level_from_score(goal.id, 65.0) == 3
            assert GoalRepository.match_level_from_score(goal.id, 70.0) == 4
            assert GoalRepository.match_level_from_score(goal.id, 80.0) == 4
            assert GoalRepository.match_level_from_score(goal.id, 85.0) == 5
            assert GoalRepository.match_level_from_score(goal.id, 100.0) == 5

    def test_independent_goal_levels(self, app):
        with app.app_context():
            goals = GoalRepository.get_all_active_goals()
            assert len(goals) == 5
            for g in goals:
                levels = GoalRepository.get_levels_for_goal(g.id)
                assert len(levels) == 5
                level_numbers = [lvl.level_number for lvl in levels]
                assert level_numbers == [1, 2, 3, 4, 5]
