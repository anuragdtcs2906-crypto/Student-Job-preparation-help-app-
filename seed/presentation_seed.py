from app.extensions import db
from app.models.content import PresentationTask

PRESENTATION_DATA = [
    # Level 1 - 1-Minute Topics & Structure
    {
        "task": "Introduce yourself to a new team in exactly 60 seconds. Include your background, what you will be working on, and one personal hobby.",
        "category": "Self-intro",
        "difficulty": "beginner",
        "level": 1,
        "evaluation_criteria": ["Engaging opening greeting", "Crisp background summary", "Warm personal note and enthusiasm"],
        "sample_outline": ["Greeting & Name (10s)", "Role & Focus Area (30s)", "Fun Fact / Hobby & closing (20s)"],
    },
    {
        "task": "Give a 1-minute talk on 'Why consistency matters more than intensity in learning new skills'.",
        "category": "1-minute topic",
        "difficulty": "beginner",
        "level": 1,
        "evaluation_criteria": ["Clear central thesis", "Relatable everyday example", "Strong concluding statement"],
        "sample_outline": ["Hook on building habits", "Example of 15 mins daily vs 5 hours once a month", "Call to action"],
    },
    {
        "task": "Present a 1-minute summary of your favorite software tool or productivity app and why someone should try it.",
        "category": "1-minute topic",
        "difficulty": "beginner",
        "level": 1,
        "evaluation_criteria": ["Problem the app solves", "Key feature highlight", "Personal impact"],
        "sample_outline": ["Name the tool and common daily frustration", "Demonstrate the core workflow benefit", "Closing recommendation"],
    },

    # Level 2 - Project Pitches & Hooks
    {
        "task": "Pitch a project you built in 2 minutes. Explain the problem, the solution, the technology used, and the impact.",
        "category": "Project pitch",
        "difficulty": "intermediate",
        "level": 2,
        "evaluation_criteria": ["Clear problem statement", "User-centric solution framing", "Tech stack overview", "Impact and demo invitation"],
        "sample_outline": ["The Problem (30s)", "Our Solution (45s)", "Tech Architecture (30s)", "Impact & Next Steps (15s)"],
    },
    {
        "task": "Present the introductory slide of a company presentation using a powerful 30-second hook (story, surprising stat, or bold question).",
        "category": "Give an introduction",
        "difficulty": "intermediate",
        "level": 2,
        "evaluation_criteria": ["Immediate audience engagement", "Seamless transition from hook to agenda", "Energetic vocal delivery"],
        "sample_outline": ["Rhetorical question or surprising metric", "Why it matters to everyone in the room", "Roadmap preview"],
    },
    {
        "task": "Explain a complex dashboard or chart slide to an executive audience in 90 seconds.",
        "category": "Explain a slide",
        "difficulty": "intermediate",
        "level": 2,
        "evaluation_criteria": ["State the main takeaway first (bottom line up front)", "Highlight 2 key data points", "State the business recommendation"],
        "sample_outline": ["One-sentence conclusion of the chart", "Direct attention to specific quadrant/trend", "Actionable next step"],
    },

    # Level 3 - Technical Concepts & Analogies
    {
        "task": "Explain the concept of 'Cloud Computing and APIs' to a non-technical audience in 2 minutes using an analogy (e.g. restaurant or electricity grid).",
        "category": "Explain a technical concept",
        "difficulty": "intermediate",
        "level": 3,
        "evaluation_criteria": ["Accessible metaphor", "Zero unexplained jargon", "Connection to everyday digital experiences"],
        "sample_outline": ["Metaphor introduction (e.g. restaurant waiter as API)", "Mapping to servers and apps", "Why this matters for reliability"],
    },
    {
        "task": "Deliver a 2-minute explanation of how 'Machine Learning differs from Traditional Programming'.",
        "category": "Two-minute topic",
        "difficulty": "intermediate",
        "level": 3,
        "evaluation_criteria": ["Clear comparison structure", "Concrete input-output examples", "Summary takeaway"],
        "sample_outline": ["Traditional rule-based logic example", "Data-driven pattern learning contrast", "Future potential"],
    },
    {
        "task": "Deliver an inspiring conclusion to a technical roadmap presentation, summarizing key milestones and issuing a call to action.",
        "category": "Give a conclusion",
        "difficulty": "intermediate",
        "level": 3,
        "evaluation_criteria": ["Recap of 3 key takeaways", "Appreciation of team efforts", "Clear immediate next action for audience"],
        "sample_outline": ["Summarize 3 core milestones", "Reiterate the shared vision", "Inspiring closing call to action"],
    },

    # Level 4 - Handling Q&A & Challenging Questions
    {
        "task": "An audience member asks: 'Your proposed database migration seems risky and expensive. Why shouldn't we keep our current system?' Deliver a calm, structured 90-second response.",
        "category": "Handle a question",
        "difficulty": "advanced",
        "level": 4,
        "evaluation_criteria": ["Validate the concern respectfully", "Reframe with long-term cost of inaction vs migration safety controls", "Offer a phased rollout safeguard"],
        "sample_outline": ["Acknowledge and thank them for the risk perspective", "Explain current bottleneck costs", "Detail zero-downtime safeguards and rollback plans"],
    },
    {
        "task": "A stakeholder interrupts during your presentation asking for a technical detail you don't know offhand. Deliver a professional, composed response that keeps the presentation on track.",
        "category": "Handle a question",
        "difficulty": "advanced",
        "level": 4,
        "evaluation_criteria": ["Graceful honesty without panicking", "Commitment to follow up with exact data", "Smooth transition back to the main presentation"],
        "sample_outline": ["Appreciate the specific question", "State current understanding and commit to exact follow-up metrics", "Resume the roadmap slide"],
    },

    # Level 5 - Keynote Delivery & Persuasion
    {
        "task": "Deliver a 3-minute keynote opening on 'The Responsibility of AI Developers in Building Ethical, Human-Centric Technology'.",
        "category": "Two-minute topic",
        "difficulty": "advanced",
        "level": 5,
        "evaluation_criteria": ["Powerful thematic narrative", "Rhetorical pacing and pauses", "Empowering call to action for the audience"],
        "sample_outline": ["Vivid story of AI impact in daily life", "The tension between rapid deployment and ethical safeguards", "The call for human-centered design principles"],
    },
]


def seed_presentation_tasks():
    """Seed presentation module tasks."""
    for item in PRESENTATION_DATA:
        existing = PresentationTask.query.filter_by(task=item["task"]).first()
        if not existing:
            t = PresentationTask(
                task=item["task"],
                category=item["category"],
                difficulty=item["difficulty"],
                level=item["level"],
                evaluation_criteria=item["evaluation_criteria"],
                sample_outline=item["sample_outline"],
            )
            db.session.add(t)
    db.session.commit()
