from app.extensions import db
from app.models.content import InterviewQuestion

INTERVIEW_DATA = [
    # Level 1 - Introduction & Core HR
    {
        "question": "Can you please walk me through your background and introduce yourself?",
        "category": "Introduction",
        "difficulty": "beginner",
        "level": 1,
        "expected_skill": "Concise present-past-future structure, professional tone",
        "evaluation_criteria": ["Current role or studies", "Key relevant projects or strengths", "Why this opportunity excites you"],
        "sample_guidance": "Use a 60-90 second structure: Start with who you are today, highlight 1-2 key accomplishments, and conclude with why you are eager for this position.",
    },
    {
        "question": "What are two of your greatest strengths, and what is one skill you are actively working to improve?",
        "category": "HR",
        "difficulty": "beginner",
        "level": 1,
        "expected_skill": "Self-awareness, constructive growth mindset",
        "evaluation_criteria": ["Specific strengths tied to real work", "Genuine area of growth with proactive action steps"],
        "sample_guidance": "Frame your growth area constructively (e.g. 'I am actively improving my presentation pacing by practicing with timers').",
    },
    {
        "question": "Why are you interested in this role and what motivated you to apply?",
        "category": "HR",
        "difficulty": "beginner",
        "level": 1,
        "expected_skill": "Role alignment, enthusiasm, company awareness",
        "evaluation_criteria": ["Connection between role and career goals", "Genuine passion for the company or domain"],
        "sample_guidance": "Mention 1 specific aspect of the team or mission that aligns with your personal values and skills.",
    },
    {
        "question": "How do you organize your tasks when you have multiple deadlines in the same week?",
        "category": "Problem Solving",
        "difficulty": "beginner",
        "level": 1,
        "expected_skill": "Time management, prioritization, communication",
        "evaluation_criteria": ["Prioritization methodology", "Use of checklists or tools", "Proactive communication with mentors/team"],
        "sample_guidance": "Explain how you distinguish between urgent vs high-impact tasks and keep stakeholders updated.",
    },
    {
        "question": "What is an accomplishment or project you are particularly proud of, and why?",
        "category": "Introduction",
        "difficulty": "beginner",
        "level": 1,
        "expected_skill": "Impact framing, enthusiasm, pride in work",
        "evaluation_criteria": ["Clear context of the project", "Your specific contribution", "What made the outcome rewarding"],
        "sample_guidance": "Focus on the hurdle you overcame and what you learned from the experience.",
    },

    # Level 2 - Behavioral & STAR Method
    {
        "question": "Tell me about a time when you had a disagreement with a team member. How did you handle it?",
        "category": "Behavioral",
        "difficulty": "intermediate",
        "level": 2,
        "expected_skill": "STAR Method, emotional intelligence, respectful resolution",
        "evaluation_criteria": ["Clear situation & task", "Constructive listening action", "Positive collaborative outcome"],
        "sample_guidance": "Use STAR: Situation, Task, Action, Result. Emphasize how you listened to their perspective first.",
    },
    {
        "question": "Describe a challenging situation where a project requirement changed midway. How did you adapt?",
        "category": "Situational",
        "difficulty": "intermediate",
        "level": 2,
        "expected_skill": "Agility, problem-solving, calm under pressure",
        "evaluation_criteria": ["Quick reassessment of goals", "Action taken to realign deliverables", "Successful delivery"],
        "sample_guidance": "Highlight how you broke down the change into manageable steps and communicated with your team.",
    },
    {
        "question": "Give an example of a time when you received constructive feedback that was difficult to hear. What did you do?",
        "category": "Behavioral",
        "difficulty": "intermediate",
        "level": 2,
        "expected_skill": "Receptivity, self-reflection, measurable improvement",
        "evaluation_criteria": ["Open mindset without defensiveness", "Tangible steps taken to implement the advice"],
        "sample_guidance": "Show your ability to separate emotion from actionable feedback and celebrate the growth that followed.",
    },
    {
        "question": "Tell me about a time you worked in a team where someone wasn't contributing their share. How did you respond?",
        "category": "Teamwork",
        "difficulty": "intermediate",
        "level": 2,
        "expected_skill": "Empathy, diplomatic communication, team accountability",
        "evaluation_criteria": ["Checking in privately rather than accusing", "Re-allocating tasks or offering support", "Team delivery"],
        "sample_guidance": "Demonstrate supportive leadership: understanding if they faced blockers and helping the team succeed together.",
    },
    {
        "question": "Can you share an experience where you had to learn a new tool or technology on a tight timeline?",
        "category": "Behavioral",
        "difficulty": "intermediate",
        "level": 2,
        "expected_skill": "Learning velocity, resourcefulness, execution",
        "evaluation_criteria": ["Systematic learning strategy", "Hands-on application", "Timely delivery"],
        "sample_guidance": "Describe your strategy for rapid learning (documentation, minimal prototypes, asking targeted questions).",
    },

    # Level 3 - Project Deep-Dives & Technical Explanations
    {
        "question": "Can you explain the architecture of a major application or project you built from scratch?",
        "category": "Project",
        "difficulty": "intermediate",
        "level": 3,
        "expected_skill": "System architecture narrative, component breakdown, trade-offs",
        "evaluation_criteria": ["High-level overview", "Key component responsibilities", "Data flow & database design", "Lessons learned"],
        "sample_guidance": "Start top-down: state the problem solved, then break down frontend, backend, database, and key technical trade-offs.",
    },
    {
        "question": "How do you explain a complex technical concept (like database indexing or caching) to a non-technical stakeholder?",
        "category": "Technical explanation",
        "difficulty": "intermediate",
        "level": 3,
        "expected_skill": "Analogy usage, jargon elimination, stakeholder empathy",
        "evaluation_criteria": ["Relatable everyday analogy", "Clear explanation of business value", "Checking for understanding"],
        "sample_guidance": "Use a clear metaphor (e.g. index in a book or library catalog) and connect it to user speed and cost savings.",
    },
    {
        "question": "Describe a difficult bug or production issue you encountered. How did you isolate and resolve it?",
        "category": "Problem solving",
        "difficulty": "intermediate",
        "level": 3,
        "expected_skill": "Root cause analysis, debugging methodology, preventative measures",
        "evaluation_criteria": ["Hypothesis testing", "Log analysis/reproduction steps", "Fix implementation and automated tests"],
        "sample_guidance": "Walk the interviewer step-by-step through your debugging hypothesis and how you prevented regressions.",
    },
    {
        "question": "When building a feature, how do you decide whether to use an existing third-party library versus writing custom code?",
        "category": "Technical explanation",
        "difficulty": "intermediate",
        "level": 3,
        "expected_skill": "Engineering judgment, maintenance costs, security evaluation",
        "evaluation_criteria": ["Evaluation of maintainability & community support", "Security and licensing risks", "Development speed vs customization"],
        "sample_guidance": "Discuss criteria: speed to market, complexity, long-term maintenance, and flexibility.",
    },
    {
        "question": "How do you ensure your code and APIs are secure and scalable?",
        "category": "Technical explanation",
        "difficulty": "intermediate",
        "level": 3,
        "expected_skill": "Security best practices, scalability fundamentals",
        "evaluation_criteria": ["Input validation & SQL injection prevention", "Authentication & token management", "Caching and indexing"],
        "sample_guidance": "Touch upon input sanitization, rate limiting, stateless authentication, and database connection pooling.",
    },

    # Level 4 - Situational Leadership & Ambiguity
    {
        "question": "Imagine you are assigned a critical project with vague requirements and tight deadlines. How would you proceed?",
        "category": "Situational",
        "difficulty": "advanced",
        "level": 4,
        "expected_skill": "Ambiguity navigation, stakeholder interviews, phased milestones",
        "evaluation_criteria": ["Requirement discovery strategy", "Creating an MVP scope", "Frequent feedback cadence with stakeholders"],
        "sample_guidance": "Explain how you create clarity from chaos: drafting a short proposal, clarifying non-negotiables, and iterating quickly.",
    },
    {
        "question": "How do you handle a situation where two senior engineers disagree strongly on architectural direction?",
        "category": "Teamwork",
        "difficulty": "advanced",
        "level": 4,
        "expected_skill": "Objective facilitation, data-driven trade-offs, consensus building",
        "evaluation_criteria": ["Defining decision criteria & constraints", "Building quick proof-of-concepts", "Documenting pros/cons objectively"],
        "sample_guidance": "Focus on de-personalizing the debate: creating a shared matrix of performance, maintainability, and delivery speed.",
    },
    {
        "question": "Tell me about a time you had to persuade leadership or team members to adopt a significant change.",
        "category": "Communication",
        "difficulty": "advanced",
        "level": 4,
        "expected_skill": "Influence without authority, business case building, empathy",
        "evaluation_criteria": ["Understanding stakeholder priorities", "Presenting data and risk mitigation", "Incremental rollout"],
        "sample_guidance": "Highlight how you tailored your pitch to their goals (e.g. cost savings, developer velocity, user satisfaction).",
    },
    {
        "question": "If you discover right before launch that a feature might cause a 5% latency increase, how do you decide whether to ship?",
        "category": "Situational",
        "difficulty": "advanced",
        "level": 4,
        "expected_skill": "Risk assessment, user impact evaluation, rollback planning",
        "evaluation_criteria": ["Analyzing critical user paths", "Evaluating feature flag / canary release options", "Collaborating with product lead"],
        "sample_guidance": "Weigh business urgency against user experience; propose mitigation such as feature-flagged gradual rollout.",
    },

    # Level 5 - Executive Presence & Strategic Vision
    {
        "question": "Where do you see the future of this industry heading in the next 3-5 years, and how do you position yourself to lead that change?",
        "category": "Situational",
        "difficulty": "advanced",
        "level": 5,
        "expected_skill": "Strategic vision, continuous innovation, proactive leadership",
        "evaluation_criteria": ["Awareness of emerging technology trends", "Strategic business implications", "Personal learning and adaptability roadmap"],
        "sample_guidance": "Deliver a concise, visionary response connecting technological trends (AI, edge computing, security) with business impact.",
    },
    {
        "question": "How do you build a culture of high engineering standards, psychological safety, and rapid innovation within a team?",
        "category": "Teamwork",
        "difficulty": "advanced",
        "level": 5,
        "expected_skill": "Leadership philosophy, blameless post-mortems, mentoring",
        "evaluation_criteria": ["Blameless root cause culture", "Pair programming and peer review standards", "Celebrating experimentation"],
        "sample_guidance": "Articulate how psychological safety and clear code ownership empower team members to take calculated risks and excel.",
    },
]


def seed_interview_questions():
    """Seed interview module questions."""
    for item in INTERVIEW_DATA:
        existing = InterviewQuestion.query.filter_by(question=item["question"]).first()
        if not existing:
            q = InterviewQuestion(
                question=item["question"],
                category=item["category"],
                difficulty=item["difficulty"],
                level=item["level"],
                expected_skill=item["expected_skill"],
                evaluation_criteria=item["evaluation_criteria"],
                sample_guidance=item["sample_guidance"],
            )
            db.session.add(q)
    db.session.commit()
