from datetime import datetime, timezone
from typing import List, Optional
from app.extensions import db
from app.models.assessment import Assessment, AssessmentQuestion, AssessmentAttempt, AssessmentAnswer


class AssessmentRepository:
    """Data access layer for Assessments, Questions, and Attempts."""

    @staticmethod
    def get_initial_assessment_for_goal(goal_id: str) -> Optional[Assessment]:
        return (
            db.session.query(Assessment)
            .filter_by(goal_id=goal_id, assessment_type="initial", is_active=True)
            .first()
        )

    @staticmethod
    def get_progression_assessment_for_goal(goal_id: str, level_number: int) -> Optional[Assessment]:
        return (
            db.session.query(Assessment)
            .filter_by(goal_id=goal_id, level_number=level_number, assessment_type="level_progression", is_active=True)
            .first()
        )

    @staticmethod
    def get_assessment_by_id(assessment_id: str) -> Optional[Assessment]:
        return db.session.query(Assessment).filter_by(id=assessment_id, is_active=True).first()

    @staticmethod
    def get_questions_for_assessment(assessment_id: str) -> List[AssessmentQuestion]:
        return (
            db.session.query(AssessmentQuestion)
            .filter_by(assessment_id=assessment_id)
            .order_by(AssessmentQuestion.display_order)
            .all()
        )

    @staticmethod
    def get_question_by_id(question_id: str) -> Optional[AssessmentQuestion]:
        return db.session.query(AssessmentQuestion).filter_by(id=question_id).first()

    @staticmethod
    def create_assessment_attempt(
        user_id: str,
        goal_id: str,
        assessment_id: Optional[str],
        assessment_type: str,
        score: float,
        total_points: float,
        percentage: float,
        calculated_level: int,
        passed_progression: Optional[bool],
        category_breakdown: dict,
        strengths: list,
        areas_to_improve: list,
        supportive_summary: str,
        ai_feedback: Optional[dict] = None,
    ) -> AssessmentAttempt:
        attempt = AssessmentAttempt(
            user_id=user_id,
            goal_id=goal_id,
            assessment_id=assessment_id,
            assessment_type=assessment_type,
            score=score,
            total_points=total_points,
            percentage=percentage,
            calculated_level=calculated_level,
            passed_progression=passed_progression,
            status="completed",
            category_breakdown=category_breakdown,
            strengths=strengths,
            areas_to_improve=areas_to_improve,
            supportive_summary=supportive_summary,
            ai_feedback=ai_feedback,
            started_at=datetime.now(timezone.utc),
            completed_at=datetime.now(timezone.utc),
        )
        db.session.add(attempt)
        db.session.commit()
        return attempt

    @staticmethod
    def add_assessment_answers(attempt_id: str, answers_data: List[dict]) -> None:
        for item in answers_data:
            ans = AssessmentAnswer(
                attempt_id=attempt_id,
                question_id=item["question_id"],
                user_response=item["user_response"],
                is_correct=item.get("is_correct"),
                score_awarded=item.get("score_awarded", 0.0),
                feedback=item.get("feedback"),
            )
            db.session.add(ans)
        db.session.commit()

    @staticmethod
    def get_latest_attempt(user_id: str, goal_id: str) -> Optional[AssessmentAttempt]:
        return (
            db.session.query(AssessmentAttempt)
            .filter_by(user_id=user_id, goal_id=goal_id)
            .order_by(AssessmentAttempt.created_at.desc() if hasattr(AssessmentAttempt, "created_at") else AssessmentAttempt.completed_at.desc())
            .first()
        )

    @staticmethod
    def get_attempts_for_user(user_id: str, goal_id: Optional[str] = None) -> List[AssessmentAttempt]:
        query = db.session.query(AssessmentAttempt).filter_by(user_id=user_id)
        if goal_id:
            query = query.filter_by(goal_id=goal_id)
        return query.order_by(AssessmentAttempt.started_at.desc()).all()
