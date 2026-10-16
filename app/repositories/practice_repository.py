from datetime import datetime, timezone, date, timedelta
from typing import List, Optional, Dict, Any
from app.extensions import db
from app.models.practice import PracticeSession, PracticeAttempt, UserProgress, UserRecommendation
from app.models.user import ActivityHistory
from app.models.ai_feedback import AIFeedback


class PracticeRepository:
    """Data access layer for practice sessions, attempts, progress, recommendations, and feedback."""

    # Sessions
    @staticmethod
    def create_session(user_id: str, goal_id: str, activity_type: str, items_target: int, session_metadata: Optional[dict] = None) -> PracticeSession:
        session = PracticeSession(
            user_id=user_id,
            goal_id=goal_id,
            activity_type=activity_type,
            items_target=items_target,
            session_metadata=session_metadata or {},
            session_start=datetime.now(timezone.utc),
            status="active",
        )
        db.session.add(session)
        db.session.commit()
        return session

    @staticmethod
    def get_session(session_id: str, user_id: str) -> Optional[PracticeSession]:
        return db.session.query(PracticeSession).filter_by(id=session_id, user_id=user_id).first()

    @staticmethod
    def get_active_session(user_id: str, goal_id: str) -> Optional[PracticeSession]:
        return (
            db.session.query(PracticeSession)
            .filter_by(user_id=user_id, goal_id=goal_id, status="active")
            .order_by(PracticeSession.session_start.desc())
            .first()
        )

    @staticmethod
    def complete_session(session_id: str, user_id: str, duration_seconds: Optional[int] = None) -> Optional[PracticeSession]:
        session = db.session.query(PracticeSession).filter_by(id=session_id, user_id=user_id).first()
        if not session:
            return None

        now = datetime.now(timezone.utc)
        session.session_end = now
        session.status = "completed"

        if duration_seconds is not None and duration_seconds >= 0:
            session.duration_seconds = duration_seconds
        elif session.session_start:
            calculated = int((now - session.session_start).total_seconds())
            session.duration_seconds = max(calculated, session.duration_seconds)

        db.session.commit()
        return session

    # Attempts
    @staticmethod
    def record_attempt(
        session_id: str,
        user_id: str,
        goal_id: str,
        content_type: str,
        content_id: str,
        user_input: Optional[str] = None,
        is_completed: bool = True,
        marked_for_revision: bool = False,
        time_spent_seconds: int = 0,
        score: Optional[float] = None,
    ) -> PracticeAttempt:
        attempt = PracticeAttempt(
            session_id=session_id,
            user_id=user_id,
            goal_id=goal_id,
            content_type=content_type,
            content_id=content_id,
            user_input=user_input,
            is_completed=is_completed,
            marked_for_revision=marked_for_revision,
            time_spent_seconds=time_spent_seconds,
            score=score,
            created_at=datetime.now(timezone.utc),
        )
        db.session.add(attempt)

        # Increment session count
        session = db.session.query(PracticeSession).filter_by(id=session_id).first()
        if session and is_completed:
            session.items_completed += 1
            session.duration_seconds += time_spent_seconds

        db.session.commit()
        return attempt

    @staticmethod
    def get_user_attempts_for_goal(user_id: str, goal_id: str, limit: int = 50) -> List[PracticeAttempt]:
        return (
            db.session.query(PracticeAttempt)
            .filter_by(user_id=user_id, goal_id=goal_id)
            .order_by(PracticeAttempt.created_at.desc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_revision_items(user_id: str, goal_id: str) -> List[PracticeAttempt]:
        return (
            db.session.query(PracticeAttempt)
            .filter_by(user_id=user_id, goal_id=goal_id, marked_for_revision=True)
            .order_by(PracticeAttempt.created_at.desc())
            .all()
        )

    # User Progress
    @staticmethod
    def get_or_create_user_progress(user_id: str, goal_id: str) -> UserProgress:
        prog = db.session.query(UserProgress).filter_by(user_id=user_id, goal_id=goal_id).first()
        if not prog:
            prog = UserProgress(
                user_id=user_id,
                goal_id=goal_id,
                total_items_completed=0,
                total_practice_time_seconds=0,
                words_practiced=0,
                questions_practiced=0,
                tasks_practiced=0,
                exercises_practiced=0,
                revision_queue_count=0,
            )
            db.session.add(prog)
            db.session.commit()
        return prog

    @staticmethod
    def update_progress_on_attempt(
        user_id: str,
        goal_id: str,
        content_type: str,
        time_spent_seconds: int,
        marked_for_revision: bool,
    ) -> UserProgress:
        prog = PracticeRepository.get_or_create_user_progress(user_id, goal_id)
        prog.total_items_completed += 1
        prog.total_practice_time_seconds += time_spent_seconds
        prog.last_practiced_at = datetime.now(timezone.utc)

        if "pronunciation" in content_type:
            prog.words_practiced += 1
        elif "interview" in content_type:
            prog.questions_practiced += 1
        elif "presentation" in content_type:
            prog.tasks_practiced += 1
        elif "communication" in content_type or "gd" in content_type:
            prog.exercises_practiced += 1

        if marked_for_revision:
            prog.revision_queue_count += 1

        db.session.commit()
        return prog

    # Activity History (Calendar)
    @staticmethod
    def record_activity_entry(user_id: str, goal_id: str, items_count: int, time_spent_seconds: int) -> ActivityHistory:
        today = date.today()
        entry = (
            db.session.query(ActivityHistory)
            .filter_by(user_id=user_id, goal_id=goal_id, activity_date=today)
            .first()
        )
        if entry:
            entry.items_completed += items_count
            entry.time_spent_seconds += time_spent_seconds
        else:
            entry = ActivityHistory(
                user_id=user_id,
                goal_id=goal_id,
                activity_date=today,
                items_completed=items_count,
                time_spent_seconds=time_spent_seconds,
            )
            db.session.add(entry)
        db.session.commit()
        return entry

    @staticmethod
    def get_activity_history(user_id: str, goal_id: Optional[str] = None, days: int = 30) -> List[ActivityHistory]:
        cutoff = date.today() - timedelta(days=days)
        query = db.session.query(ActivityHistory).filter(
            ActivityHistory.user_id == user_id,
            ActivityHistory.activity_date >= cutoff,
        )
        if goal_id:
            query = query.filter(ActivityHistory.goal_id == goal_id)
        return query.order_by(ActivityHistory.activity_date.asc()).all()

    # Recommendations
    @staticmethod
    def save_recommendations(user_id: str, goal_id: str, recommendations_data: List[dict]) -> List[UserRecommendation]:
        # Clear previously unconsumed recommendations for this user & goal
        db.session.query(UserRecommendation).filter_by(user_id=user_id, goal_id=goal_id, is_consumed=False).delete()

        created = []
        for rec in recommendations_data:
            r = UserRecommendation(
                user_id=user_id,
                goal_id=goal_id,
                content_type=rec["content_type"],
                content_id=rec["content_id"],
                reason=rec["reason"],
                reason_label=rec.get("reason_label"),
                priority=rec.get("priority", 1),
            )
            db.session.add(r)
            created.append(r)
        db.session.commit()
        return created

    @staticmethod
    def get_user_recommendations(user_id: str, goal_id: str, limit: int = 20) -> List[UserRecommendation]:
        return (
            db.session.query(UserRecommendation)
            .filter_by(user_id=user_id, goal_id=goal_id, is_consumed=False)
            .order_by(UserRecommendation.priority.desc(), UserRecommendation.created_at.desc())
            .limit(limit)
            .all()
        )

    # AI Feedback
    @staticmethod
    def save_ai_feedback(
        user_id: str,
        goal_id: str,
        source_type: str,
        source_id: str,
        strengths: list,
        areas_to_improve: list,
        feedback_text: str,
        recommended_practice: list,
        confidence_message: str,
        model_used: str = "gpt-4o-mini",
        practice_attempt_id: Optional[str] = None,
    ) -> AIFeedback:
        fb = AIFeedback(
            user_id=user_id,
            goal_id=goal_id,
            source_type=source_type,
            source_id=source_id,
            practice_attempt_id=practice_attempt_id,
            strengths=strengths,
            areas_to_improve=areas_to_improve,
            feedback_text=feedback_text,
            recommended_practice=recommended_practice,
            confidence_message=confidence_message,
            model_used=model_used,
        )
        db.session.add(fb)
        db.session.commit()
        return fb
