import pytest
from app.recommendation.strategies import RecommendationStrategy
from app.recommendation.engine import RecommendationEngine
from app.repositories.user_repository import UserRepository
from app.repositories.goal_repository import GoalRepository
from app.repositories.practice_repository import PracticeRepository


class TestRecommendationEngine:
    def test_distribution_calculation(self):
        # 10 items with revision and difficult
        dist = RecommendationStrategy.calculate_distribution(10, has_revision=True, has_difficult=True)
        assert dist["new"] + dist["difficult"] + dist["revision"] == 10
        assert dist["new"] >= 4
        assert dist["difficult"] >= 2
        assert dist["revision"] >= 1

        # 5 items with only revision
        dist2 = RecommendationStrategy.calculate_distribution(5, has_revision=True, has_difficult=False)
        assert dist2["new"] + dist2["revision"] == 5

        # 10 items without prior history (all new)
        dist3 = RecommendationStrategy.calculate_distribution(10, has_revision=False, has_difficult=False)
        assert dist3["new"] == 10
        assert dist3["difficult"] == 0
        assert dist3["revision"] == 0

    def test_generate_recommendations_for_user(self, app):
        with app.app_context():
            user = UserRepository.create_anonymous_user()
            goal = GoalRepository.get_by_slug("pronunciation")
            UserRepository.get_or_create_user_goal(user.id, goal.id)

            recs = RecommendationEngine.generate_recommendations(user.id, "pronunciation", limit_override=5)
            assert len(recs) == 5
            for r in recs:
                assert "content_id" in r
                assert "content_type" in r
                assert "reason" in r
                assert "content" in r
                assert r["content"] is not None
