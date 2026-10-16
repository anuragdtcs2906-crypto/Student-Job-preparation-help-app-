from typing import Dict, Any, Optional, List
from app.repositories.goal_repository import GoalRepository
from app.repositories.user_repository import UserRepository
from app.repositories.practice_repository import PracticeRepository
from app.ai.feedback_engine import AIFeedbackEngine
from app.utils.exceptions import NotFoundError, ValidationError


class PracticeService:
    """Service managing practice sessions, attempts, and integrated AI feedback."""

    def __init__(self, feedback_engine: Optional[AIFeedbackEngine] = None):
        self.feedback_engine = feedback_engine or AIFeedbackEngine()

    def start_session(
        self,
        user_id: str,
        goal_slug: str,
        activity_type: Optional[str] = None,
        target_count: Optional[int] = None,
        session_metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        goal = GoalRepository.get_by_slug(goal_slug)
        if not goal:
            raise NotFoundError(f"Goal '{goal_slug}' not found.")

        # If user has an active session for this goal, return it or close it
        active_sess = PracticeRepository.get_active_session(user_id, goal.id)
        if active_sess:
            return active_sess.to_dict(include_attempts=True)

        daily_target = UserRepository.get_daily_target(user_id, goal.id)
        target = target_count or (daily_target.target_quantity if daily_target else goal.default_target_quantity)
        activity = activity_type or goal.slug

        session = PracticeRepository.create_session(
            user_id=user_id,
            goal_id=goal.id,
            activity_type=activity,
            items_target=target,
            session_metadata=session_metadata or {},
        )
        return session.to_dict()

    def record_attempt(
        self,
        user_id: str,
        session_id: str,
        content_type: str,
        content_id: str,
        user_input: Optional[str] = None,
        is_completed: bool = True,
        marked_for_revision: bool = False,
        time_spent_seconds: int = 0,
        request_ai_feedback: bool = False,
    ) -> Dict[str, Any]:
        session = PracticeRepository.get_session(session_id, user_id)
        if not session:
            raise NotFoundError("Practice session not found or does not belong to this user.")

        goal_id = session.goal_id
        goal_slug = session.goal.slug if session.goal else "interview"

        # Record attempt in database
        attempt = PracticeRepository.record_attempt(
            session_id=session_id,
            user_id=user_id,
            goal_id=goal_id,
            content_type=content_type,
            content_id=content_id,
            user_input=user_input,
            is_completed=is_completed,
            marked_for_revision=marked_for_revision,
            time_spent_seconds=time_spent_seconds,
        )

        # Update cumulative progress and calendar activity
        PracticeRepository.update_progress_on_attempt(
            user_id=user_id,
            goal_id=goal_id,
            content_type=content_type,
            time_spent_seconds=time_spent_seconds,
            marked_for_revision=marked_for_revision,
        )

        PracticeRepository.record_activity_entry(
            user_id=user_id,
            goal_id=goal_id,
            items_count=1 if is_completed else 0,
            time_spent_seconds=time_spent_seconds,
        )

        # Generate AI Feedback if requested and user input is present
        ai_feedback = None
        if request_ai_feedback and user_input and len(user_input.strip()) > 3:
            user_goal = UserRepository.get_user_goal_by_slug(user_id, goal_slug)
            current_level = user_goal.current_level if user_goal else 1

            ai_feedback = self.feedback_engine.evaluate_response(
                user_id=user_id,
                goal_id=goal_id,
                goal_slug=goal_slug,
                prompt_context=f"Practice item ({content_type}) ID: {content_id}",
                user_response=user_input,
                level=current_level,
                source_type="practice_attempt",
                source_id=attempt.id,
                practice_attempt_id=attempt.id,
                save_to_db=True,
            )

        attempt_dict = attempt.to_dict()
        if ai_feedback:
            attempt_dict["feedback"] = ai_feedback

        return attempt_dict

    def complete_session(
        self,
        user_id: str,
        session_id: str,
        duration_seconds: Optional[int] = None,
    ) -> Dict[str, Any]:
        session = PracticeRepository.complete_session(session_id, user_id, duration_seconds)
        if not session:
            raise NotFoundError("Practice session not found.")
        return session.to_dict(include_attempts=True)
