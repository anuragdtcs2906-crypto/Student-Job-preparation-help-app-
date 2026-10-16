from app.extensions import db
from app.models.content import GDQuestion

GD_DATA = [
    # Level 1 - Stating Opinions & Entering Discussions
    {
        "topic": "Remote vs Hybrid vs In-Office Work Models",
        "scenario": "Your group has been debating remote work. Enter the discussion politely to state your viewpoint on the benefits of hybrid work for team collaboration.",
        "category": "Opinion",
        "difficulty": "beginner",
        "level": 1,
        "perspective_points": [
            "Flexibility boosts individual deep work productivity",
            "In-person collaboration accelerates brainstorming and relationship building",
            "Hybrid model strikes a balanced middle ground",
        ],
        "evaluation_criteria": ["Polite entry phrase", "Clear, concise opinion", "Concrete supporting reason"],
    },
    {
        "topic": "Should Artificial Intelligence Tools be Taught in High Schools?",
        "scenario": "Initiate the discussion by stating your perspective on how early AI literacy prepares students for future careers.",
        "category": "Opinion",
        "difficulty": "beginner",
        "level": 1,
        "perspective_points": [
            "AI literacy teaches critical thinking and prompt framing",
            "Understanding AI ethics and bias early creates responsible digital citizens",
            "Balancing AI tools with fundamental learning basics",
        ],
        "evaluation_criteria": ["Engaging opening statement", "Logical flow", "Inviting others to share their views"],
    },

    # Level 2 - Respectful Agreement & Disagreement
    {
        "topic": "Prioritizing Speed to Market vs 100% Feature Perfection in Startups",
        "scenario": "A colleague argues: 'We should never ship a product until every single bug is eliminated.' Express respectful disagreement by advocating for iterative MVP testing.",
        "category": "Disagreeing respectfully",
        "difficulty": "intermediate",
        "level": 2,
        "perspective_points": [
            "Real user feedback is more valuable than internal assumptions",
            "Core functionality must be rock-solid, while secondary features can evolve",
            "Over-polishing delays learning from actual market dynamics",
        ],
        "evaluation_criteria": ["Acknowledge their valid point on quality first", "Use diplomatic disagreement phrasing", "Provide reasoned counter-argument"],
    },
    {
        "topic": "Are Strict Deadlines Better for Creativity Than Flexible Schedules?",
        "scenario": "A participant states that deadlines kill all creative ideas. Agree partially while explaining how structured constraints often channel creativity effectively.",
        "category": "Agreeing",
        "difficulty": "intermediate",
        "level": 2,
        "perspective_points": [
            "Unbounded time can lead to perfectionism and indecision",
            "Constraints force innovative prioritization",
            "Balanced checkpoints provide safety buffers",
        ],
        "evaluation_criteria": ["Nuanced agreement ('I agree that excessive pressure is harmful, but...')", "Balanced synthesis"],
    },

    # Level 3 - Building on Points & Asking Clarifications
    {
        "topic": "Cashless Society & Digital Currency: Opportunities and Inclusivity",
        "scenario": "A participant just gave statistics on digital transaction growth. Build upon their point by addressing how to ensure elderly or rural populations remain included.",
        "category": "Adding a point",
        "difficulty": "intermediate",
        "level": 3,
        "perspective_points": [
            "Digital payments increase transparency and convenience",
            "Infrastructure and accessibility gaps need targeted offline support",
            "Cybersecurity awareness must grow alongside adoption",
        ],
        "evaluation_criteria": ["Explicit reference to previous speaker's point", "Seamless additive connection", "Actionable perspective"],
    },
    {
        "topic": "Data Privacy vs Hyper-Personalized AI Recommendations",
        "scenario": "A speaker mentions that users love personalization. Ask a thoughtful clarifying question about user consent and data retention boundaries.",
        "category": "Asking clarification",
        "difficulty": "intermediate",
        "level": 3,
        "perspective_points": [
            "Personalization adds convenience and discovery",
            "Transparency in how data is processed builds long-term user trust",
            "Granular user control over data sharing settings",
        ],
        "evaluation_criteria": ["Curious, respectful tone", "Insightful question that advances the discussion"],
    },

    # Level 4 - Summarizing & Moderating Discussions
    {
        "topic": "Balancing Renewable Energy Transition with Short-Term Industrial Demands",
        "scenario": "The discussion has become fragmented between environmental advocates and industrial representatives. Step in to summarize the two opposing views and propose a phased consensus.",
        "category": "Summarizing",
        "difficulty": "advanced",
        "level": 4,
        "perspective_points": [
            "Urgent environmental imperative for clean energy",
            "Economic necessity of preserving grid stability and jobs",
            "Phased transition with government incentives and hybrid power",
        ],
        "evaluation_criteria": ["Neutral, balanced summary of both sides", "Concise synthesis in 3 points", "Consensus proposal"],
    },
    {
        "topic": "Workplace Teamwork: Resolving Ownership Conflicts Across Cross-Functional Teams",
        "scenario": "The design team and engineering team are locked in a debate over who decides final UX implementation. Propose a collaborative framework to align both teams.",
        "category": "Teamwork",
        "difficulty": "advanced",
        "level": 4,
        "perspective_points": [
            "Design brings deep empathy for user friction",
            "Engineering brings feasibility and system performance constraints",
            "Shared user-metric goals (e.g. task completion rate) unify efforts",
        ],
        "evaluation_criteria": ["De-escalation tone", "Focus on shared customer outcome", "Clear decision framework (e.g. RACI matrix)"],
    },

    # Level 5 - Executive Roundtables & High-Stakes Leadership
    {
        "topic": "Leading Organizational Transformation Through Generative AI Adoption",
        "scenario": "In an executive roundtable, present a compelling 2-minute strategic viewpoint on how to upskill the workforce rather than displacing employees with automation.",
        "category": "Speaking concisely",
        "difficulty": "advanced",
        "level": 5,
        "perspective_points": [
            "AI as a cognitive amplifier for human talent",
            "Structured internal upskilling programs create competitive moats",
            "Culture of experimentation paired with clear ethical guardrails",
        ],
        "evaluation_criteria": ["Executive poise", "Empowering human-centered vision", "High-impact concise delivery"],
    },
]


def seed_gd_questions():
    """Seed group discussion module questions."""
    for item in GD_DATA:
        existing = GDQuestion.query.filter_by(topic=item["topic"]).first()
        if not existing:
            g = GDQuestion(
                topic=item["topic"],
                scenario=item["scenario"],
                category=item["category"],
                difficulty=item["difficulty"],
                level=item["level"],
                perspective_points=item["perspective_points"],
                evaluation_criteria=item["evaluation_criteria"],
            )
            db.session.add(g)
    db.session.commit()
