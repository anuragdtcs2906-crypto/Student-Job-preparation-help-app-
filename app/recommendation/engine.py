from typing import List, Dict, Any, Optional
import pandas as pd
import numpy as np

from app.models.content import (
    PronunciationWord,
    InterviewQuestion,
    PresentationTask,
    CommunicationExercise,
    GDQuestion,
)
from app.models.practice import PracticeAttempt
from app.models.user import DailyTarget, UserGoal
from app.repositories.goal_repository import GoalRepository
from app.repositories.user_repository import UserRepository
from app.repositories.practice_repository import PracticeRepository
from app.recommendation.strategies import RecommendationStrategy, RecommendationItem
from app.extensions import db


class RecommendationEngine:
    """
    AI & Rule-Based Personalization Engine.
    Combines:
    - User's Goal & Current Level
    - Diagnostic Assessment Strengths/Focus Areas
    - Historical Practice Attempts & Revision Queue
    - Daily Practice Target Quantity
    """

    @classmethod
    def generate_recommendations(
        cls,
        user_id: str,
        goal_slug: str,
        limit_override: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        goal = GoalRepository.get_by_slug(goal_slug)
        if not goal:
            return []

        user_goal = UserRepository.get_user_goal_by_slug(user_id, goal_slug)
        current_level = user_goal.current_level if user_goal else 1

        daily_target = UserRepository.get_daily_target(user_id, goal.id)
        target_quantity = limit_override or (daily_target.target_quantity if daily_target else goal.default_target_quantity)

        # 1. Fetch user's practice history for this goal
        past_attempts = PracticeRepository.get_user_attempts_for_goal(user_id, goal.id, limit=200)
        practiced_ids = set()
        revision_ids = set()
        low_score_ids = set()

        for att in past_attempts:
            practiced_ids.add(att.content_id)
            if att.marked_for_revision:
                revision_ids.add(att.content_id)
            if att.score is not None and att.score < 60.0:
                low_score_ids.add(att.content_id)

        # 2. Query available content based on goal type
        content_type, pool_items = cls._fetch_content_pool(goal_slug, current_level)
        if not pool_items:
            return []

        # Convert pool to DataFrame for systematic filtering
        items_dict_map = {item.id: item.to_dict() for item in pool_items}
        
        # 3. Categorize available items
        new_items = []
        difficult_items = []
        revision_items = []

        for item in pool_items:
            item_id = item.id
            if item_id in low_score_ids:
                difficult_items.append(item)
            elif item_id in revision_ids:
                revision_items.append(item)
            elif item_id not in practiced_ids:
                new_items.append(item)

        # If we have exhausted all unpracticed items, allow re-practicing earlier items
        if not new_items:
            new_items = [item for item in pool_items if item.id not in revision_ids and item.id not in low_score_ids]

        # 4. Calculate distribution quotas
        distribution = RecommendationStrategy.calculate_distribution(
            target_count=target_quantity,
            has_revision=bool(revision_items),
            has_difficult=bool(difficult_items),
        )

        selected_recs: List[RecommendationItem] = []

        # Add Difficult Items
        for item in difficult_items[: distribution["difficult"]]:
            selected_recs.append(
                RecommendationItem(
                    content_id=item.id,
                    content_type=content_type,
                    reason="difficult_item",
                    reason_label=f"Strengthen this Level {getattr(item, 'level', current_level)} skill",
                    priority=4,
                    data=items_dict_map.get(item.id),
                )
            )

        # Add Revision Items
        for item in revision_items[: distribution["revision"]]:
            selected_recs.append(
                RecommendationItem(
                    content_id=item.id,
                    content_type=content_type,
                    reason="spaced_revision",
                    reason_label="Spaced practice for mastery retention",
                    priority=3,
                    data=items_dict_map.get(item.id),
                )
            )

        # Add New Level-Appropriate Items
        remaining_slots = target_quantity - len(selected_recs)
        for item in new_items[:remaining_slots]:
            selected_recs.append(
                RecommendationItem(
                    content_id=item.id,
                    content_type=content_type,
                    reason="new_level",
                    reason_label=f"Core Level {getattr(item, 'level', current_level)} practice",
                    priority=5,
                    data=items_dict_map.get(item.id),
                )
            )

        # Fallback if still under target
        if len(selected_recs) < target_quantity:
            used_ids = {r.content_id for r in selected_recs}
            for item in pool_items:
                if item.id not in used_ids:
                    selected_recs.append(
                        RecommendationItem(
                            content_id=item.id,
                            content_type=content_type,
                            reason="target_fulfillment",
                            reason_label=f"Level {getattr(item, 'level', current_level)} practice",
                            priority=2,
                            data=items_dict_map.get(item.id),
                        )
                    )
                if len(selected_recs) >= target_quantity:
                    break

        # 5. Persist recommendations to database
        db_records_data = [
            {
                "content_type": r.content_type,
                "content_id": r.content_id,
                "reason": r.reason,
                "reason_label": r.reason_label,
                "priority": r.priority,
            }
            for r in selected_recs
        ]
        PracticeRepository.save_recommendations(user_id, goal.id, db_records_data)

        # Return rich output including content payload
        return [
            {
                "content_id": r.content_id,
                "content_type": r.content_type,
                "reason": r.reason,
                "reason_label": r.reason_label,
                "priority": r.priority,
                "content": r.data,
            }
            for r in selected_recs
        ]

    @staticmethod
    def _fetch_content_pool(goal_slug: str, current_level: int):
        """Fetch all content items matching level and adjacent review levels."""
        # Include current level items, plus level - 1 for revision if level > 1
        levels_to_fetch = [current_level]
        if current_level > 1:
            levels_to_fetch.append(current_level - 1)

        if goal_slug == "pronunciation":
            items = (
                db.session.query(PronunciationWord)
                .filter(PronunciationWord.level.in_(levels_to_fetch), PronunciationWord.is_active == True)
                .all()
            )
            return "pronunciation_words", items

        elif goal_slug == "interview":
            items = (
                db.session.query(InterviewQuestion)
                .filter(InterviewQuestion.level.in_(levels_to_fetch), InterviewQuestion.is_active == True)
                .all()
            )
            return "interview_questions", items

        elif goal_slug == "presentation":
            items = (
                db.session.query(PresentationTask)
                .filter(PresentationTask.level.in_(levels_to_fetch), PresentationTask.is_active == True)
                .all()
            )
            return "presentation_tasks", items

        elif goal_slug == "communication":
            items = (
                db.session.query(CommunicationExercise)
                .filter(CommunicationExercise.level.in_(levels_to_fetch), CommunicationExercise.is_active == True)
                .all()
            )
            return "communication_exercises", items

        elif goal_slug == "gd":
            items = (
                db.session.query(GDQuestion)
                .filter(GDQuestion.level.in_(levels_to_fetch), GDQuestion.is_active == True)
                .all()
            )
            return "gd_questions", items

        return "", []
