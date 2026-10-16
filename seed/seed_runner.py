import logging
import os
import sys

# Ensure root directory is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extensions import db
from seed.goals_seed import seed_goals
from seed.pronunciation_seed import seed_pronunciation_words
from seed.interview_seed import seed_interview_questions
from seed.presentation_seed import seed_presentation_tasks
from seed.communication_seed import seed_communication_exercises
from seed.gd_seed import seed_gd_questions
from seed.assessment_seed import seed_assessments

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_all_seeds():
    """Run all database seeders idempotently."""
    logger.info("Starting database seeding...")
    db.create_all()

    logger.info("1/7 Seeding Goals, Levels, and Level Configurations...")
    seed_goals()

    logger.info("2/7 Seeding Pronunciation dataset...")
    seed_pronunciation_words()

    logger.info("3/7 Seeding Interview questions dataset...")
    seed_interview_questions()

    logger.info("4/7 Seeding Presentation tasks dataset...")
    seed_presentation_tasks()

    logger.info("5/7 Seeding Clear English communication exercises...")
    seed_communication_exercises()

    logger.info("6/7 Seeding Group Discussion scenarios...")
    seed_gd_questions()

    logger.info("7/7 Seeding Diagnostic and Progression Assessments...")
    seed_assessments()

    logger.info("Database seeding completed successfully!")


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        run_all_seeds()
