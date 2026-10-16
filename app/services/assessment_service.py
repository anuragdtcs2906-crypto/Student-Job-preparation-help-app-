from typing import List, Dict, Any, Optional
from app.repositories.goal_repository import GoalRepository
from app.repositories.user_repository import UserRepository
from app.repositories.assessment_repository import AssessmentRepository
from app.ai.assessment_helper import AIAssessmentHelper
from app.recommendation.engine import RecommendationEngine
from app.utils.exceptions import NotFoundError, ValidationError, AssessmentError
from app.extensions import db


class AssessmentService:
    """
    Service handling diagnostic assessments and level progression checks.
    Level calculations are strictly deterministic and rule-configured.
    """

    def __init__(self, assessment_helper: Optional[AIAssessmentHelper] = None):
        self.assessment_helper = assessment_helper or AIAssessmentHelper()

    def get_diagnostic_assessment(self, goal_slug: str) -> Dict[str, Any]:
        goal = GoalRepository.get_by_slug(goal_slug)
        if not goal:
            raise NotFoundError(f"Goal '{goal_slug}' not found.")

        assessment = AssessmentRepository.get_initial_assessment_for_goal(goal.id)
        if not assessment:
            raise NotFoundError(f"No diagnostic assessment found for goal '{goal_slug}'.")

        return assessment.to_dict(include_questions=True)

    def get_progression_assessment(self, goal_slug: str, level_number: int) -> Dict[str, Any]:
        goal = GoalRepository.get_by_slug(goal_slug)
        if not goal:
            raise NotFoundError(f"Goal '{goal_slug}' not found.")

        assessment = AssessmentRepository.get_progression_assessment_for_goal(goal.id, level_number)
        if not assessment:
            raise NotFoundError(f"No level progression assessment found for {goal_slug} Level {level_number}.")

        return assessment.to_dict(include_questions=True)

    def submit_assessment(
        self,
        user_id: str,
        goal_slug: str,
        assessment_id: Optional[str],
        answers_payload: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        goal = GoalRepository.get_by_slug(goal_slug)
        if not goal:
            raise NotFoundError(f"Goal '{goal_slug}' not found.")

        user_goal = UserRepository.get_user_goal_by_slug(user_id, goal_slug)
        if not user_goal:
            user_goal = UserRepository.get_or_create_user_goal(user_id, goal.id)

        assessment = None
        if assessment_id:
            assessment = AssessmentRepository.get_assessment_by_id(assessment_id)
        if not assessment:
            assessment = AssessmentRepository.get_initial_assessment_for_goal(goal.id)

        if not assessment:
            raise AssessmentError(f"Assessment not found for goal '{goal_slug}'.")

        questions = AssessmentRepository.get_questions_for_assessment(assessment.id)
        if not questions:
            raise AssessmentError("Assessment has no questions configured.")

        questions_by_id = {q.id: q for q in questions}

        # Calculate scores per question and by category
        earned_score = 0.0
        total_possible = 0.0
        category_stats: Dict[str, Dict[str, float]] = {}
        processed_answers = []

        for item in answers_payload:
            q_id = item.get("question_id")
            user_resp = item.get("user_response")
            question = questions_by_id.get(q_id)
            if not question:
                continue

            q_points = float(question.points)
            total_possible += q_points
            cat = question.category

            if cat not in category_stats:
                category_stats[cat] = {"score": 0.0, "total": 0.0}
            category_stats[cat]["total"] += q_points

            # Deterministic Answer Scoring
            is_correct, awarded_score, feedback = self._score_question(question, user_resp)
            earned_score += awarded_score
            category_stats[cat]["score"] += awarded_score

            processed_answers.append({
                "question_id": q_id,
                "user_response": user_resp,
                "is_correct": is_correct,
                "score_awarded": awarded_score,
                "feedback": feedback,
            })

        if total_possible == 0:
            total_possible = 100.0

        percentage = round((earned_score / total_possible) * 100, 1)

        # Compute Category Breakdown Percentages
        category_breakdown = {}
        strengths = []
        areas_to_improve = []

        for cat, stats in category_stats.items():
            cat_total = stats["total"]
            cat_score = stats["score"]
            cat_pct = round((cat_score / cat_total) * 100, 1) if cat_total > 0 else 0.0
            category_breakdown[cat] = {
                "score": cat_score,
                "total": cat_total,
                "percentage": cat_pct,
            }
            if cat_pct >= 65.0:
                strengths.append(f"Solid grasp of {cat}")
            else:
                areas_to_improve.append(f"Strengthen {cat}")

        # Deterministic Level Assignment
        is_progression = (assessment.assessment_type == "level_progression")
        passed_progression = None

        if is_progression:
            passed_progression = percentage >= assessment.pass_percentage
            if passed_progression:
                new_level = min(5, (assessment.level_number or user_goal.current_level) + 1)
                user_goal.current_level = new_level
                calculated_level = new_level
            else:
                calculated_level = user_goal.current_level
        else:
            # Initial diagnostic assessment
            calculated_level = GoalRepository.match_level_from_score(goal.id, percentage)
            user_goal.starting_level = calculated_level
            user_goal.current_level = calculated_level
            user_goal.assessment_status = "completed"

        db.session.commit()

        # Generate qualitative supportive summary
        ai_summary = self.assessment_helper.generate_assessment_summary(
            goal_slug=goal_slug,
            assigned_level=calculated_level,
            percentage=percentage,
            category_breakdown=category_breakdown,
            strengths=strengths,
            areas_to_improve=areas_to_improve,
        )

        supportive_message = ai_summary.get("summary_text")

        # Persist Attempt
        attempt = AssessmentRepository.create_assessment_attempt(
            user_id=user_id,
            goal_id=goal.id,
            assessment_id=assessment.id,
            assessment_type=assessment.assessment_type,
            score=earned_score,
            total_points=total_possible,
            percentage=percentage,
            calculated_level=calculated_level,
            passed_progression=passed_progression,
            category_breakdown=category_breakdown,
            strengths=strengths,
            areas_to_improve=areas_to_improve,
            supportive_summary=supportive_message,
            ai_feedback=ai_summary,
        )

        AssessmentRepository.add_assessment_answers(attempt.id, processed_answers)

        # Trigger personalized recommendation generation
        recommendations = RecommendationEngine.generate_recommendations(user_id, goal_slug)

        return {
            "attempt_id": attempt.id,
            "goal_slug": goal_slug,
            "assessment_type": assessment.assessment_type,
            "score": earned_score,
            "total_points": total_possible,
            "percentage": percentage,
            "calculated_level": calculated_level,
            "passed_progression": passed_progression,
            "category_breakdown": category_breakdown,
            "strengths": strengths,
            "areas_to_improve": areas_to_improve,
            "supportive_summary": supportive_message,
            "initial_recommendations_count": len(recommendations),
        }

    def _score_question(self, question, user_resp) -> tuple:
        """
        Deterministic scoring of individual question responses.
        """
        q_type = question.question_type
        correct = question.correct_answer
        points = float(question.points)

        if not user_resp:
            return False, 0.0, "No response provided."

        if q_type in ("multiple_choice", "stress_choice", "syllable_count", "sentence_choice"):
            if isinstance(correct, dict):
                expected = correct.get("key") or correct.get("value") or correct.get("answer")
            else:
                expected = correct

            if isinstance(user_resp, dict):
                actual = user_resp.get("key") or user_resp.get("value") or user_resp.get("answer")
            else:
                actual = user_resp

            if str(actual).strip().lower() == str(expected).strip().lower():
                return True, points, "Correct!"
            return False, 0.0, f"Suggested answer: {expected}"

        elif q_type == "open_ended":
            # For diagnostic open-ended, assess completion and length
            resp_str = str(user_resp).strip()
            word_count = len(resp_str.split())
            if word_count >= 15:
                return True, points, "Great, thoughtful expression!"
            elif word_count >= 5:
                return True, points * 0.7, "Good start; adding a bit more detail will make your point even stronger."
            else:
                return False, points * 0.4, "Brief response provided."

        return True, points, "Response recorded."
