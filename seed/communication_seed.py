from app.extensions import db
from app.models.content import CommunicationExercise

COMMUNICATION_DATA = [
    # Level 1 - Sentence Construction & Basic Clarity
    {
        "exercise_type": "sentence_improvement",
        "prompt": "Improve this wordy and unclear sentence: 'Due to the fact that there was a delay in the delivery, we were not able to finish the work on time.'",
        "options": [
            {"key": "A", "text": "Because the delivery was delayed, we could not finish the work on time."},
            {"key": "B", "text": "Owing to delivery delay facts, finishing on time was not something we were able to do."},
            {"key": "C", "text": "Delayed delivery happened so we did not finish work."},
            {"key": "D", "text": "The delivery was delayed therefore on-time work completion was unable to happen."},
        ],
        "correct_answer": "A",
        "explanation": "Option A replaces the verbose phrase 'Due to the fact that' with a crisp, direct 'Because', making the sentence concise and natural.",
        "category": "Sentence Improvement",
        "difficulty": "beginner",
        "level": 1,
    },
    {
        "exercise_type": "sentence_construction",
        "prompt": "Arrange the words into a grammatically clear and natural professional update: [the project / completed / we / successfully / yesterday].",
        "options": [
            {"key": "A", "text": "We successfully completed the project yesterday."},
            {"key": "B", "text": "Yesterday completed we the project successfully."},
            {"key": "C", "text": "The project yesterday successfully we completed."},
            {"key": "D", "text": "We completed yesterday successfully the project."},
        ],
        "correct_answer": "A",
        "explanation": "Standard English S-V-O order with the adverb 'successfully' modifying the verb 'completed' before the direct object and time marker.",
        "category": "Sentence Construction",
        "difficulty": "beginner",
        "level": 1,
    },
    {
        "exercise_type": "everyday_communication",
        "prompt": "You missed a quick detail in a team meeting. What is the most polite and natural way to ask the speaker to repeat it?",
        "options": [
            {"key": "A", "text": "What did you say? Repeat again."},
            {"key": "B", "text": "Could you please clarify that last point once more?"},
            {"key": "C", "text": "I didn't hear you, speak louder."},
            {"key": "D", "text": "Say it again please."},
        ],
        "correct_answer": "B",
        "explanation": "Option B uses 'Could you please clarify...' which is warm, professional, and respectful in collaborative settings.",
        "category": "Everyday Communication",
        "difficulty": "beginner",
        "level": 1,
    },

    # Level 2 - Professional Workplace Vocabulary
    {
        "exercise_type": "vocabulary",
        "prompt": "Choose the most professional word to replace 'fix' in: 'We need to [fix] the discrepancy in the quarterly financial report.'",
        "options": [
            {"key": "A", "text": "patch up"},
            {"key": "B", "text": "reconcile"},
            {"key": "C", "text": "do something to"},
            {"key": "D", "text": "fiddle with"},
        ],
        "correct_answer": "B",
        "explanation": "'Reconcile' is the precise professional term for resolving numerical or factual discrepancies in reports.",
        "category": "Vocabulary",
        "difficulty": "intermediate",
        "level": 2,
    },
    {
        "exercise_type": "professional_communication",
        "prompt": "You need feedback from a manager who is very busy. Which email subject line and opening is most effective?",
        "options": [
            {"key": "A", "text": "Subject: Read this ASAP! / Opening: I need your answer right away."},
            {"key": "B", "text": "Subject: Urgent review required / Opening: Why haven't you replied yet?"},
            {"key": "C", "text": "Subject: [Quick Review] 2-min feedback on Q3 Design Draft / Opening: Hi Alex, hope your week is going well. When you have 2 minutes, I would appreciate your thoughts on..."},
            {"key": "D", "text": "Subject: Hey / Opening: Look at the attached file."},
        ],
        "correct_answer": "C",
        "explanation": "Option C sets a clear expectation of time commitment ('2-min feedback') with an organized, courteous greeting.",
        "category": "Professional Communication",
        "difficulty": "intermediate",
        "level": 2,
    },

    # Level 3 - Concise Expression & Active Voice
    {
        "exercise_type": "sentence_improvement",
        "prompt": "Convert this passive sentence to active voice for greater impact: 'The new optimization feature was implemented by our engineering team to reduce latency.'",
        "options": [
            {"key": "A", "text": "Our engineering team implemented the new optimization feature to reduce latency."},
            {"key": "B", "text": "To reduce latency, implementation of the feature was done by our team."},
            {"key": "C", "text": "By our engineering team, the feature reduction latency was implemented."},
            {"key": "D", "text": "The new feature had been implemented by engineers reducing latency."},
        ],
        "correct_answer": "A",
        "explanation": "Option A places the active subject ('Our engineering team') at the front, creating a punchy, confident statement.",
        "category": "Sentence Improvement",
        "difficulty": "intermediate",
        "level": 3,
    },
    {
        "exercise_type": "response_selection",
        "prompt": "A client asks if a requested custom feature is possible within 2 weeks. It is feasible, but requires simplifying secondary requirements. How do you respond clearly?",
        "options": [
            {"key": "A", "text": "No, two weeks is impossible unless you give up everything."},
            {"key": "B", "text": "Yes, we can definitely deliver the core functionality within two weeks by focusing on primary user flows first and scheduling advanced customizations for phase two."},
            {"key": "C", "text": "We will try our best and maybe it will happen or maybe not."},
            {"key": "D", "text": "Sure whatever you want we will do it."},
        ],
        "correct_answer": "B",
        "explanation": "Option B provides a constructive, solution-oriented timeline with clear prioritization.",
        "category": "Response Selection",
        "difficulty": "intermediate",
        "level": 3,
    },

    # Level 4 - Diplomatic Phrasing & Workplace Dialogue
    {
        "exercise_type": "professional_communication",
        "prompt": "A colleague's proposal has an overlooked flaw that could cause database deadlocks. How do you raise this diplomatically during a code review?",
        "options": [
            {"key": "A", "text": "This design is wrong and will break our database."},
            {"key": "B", "text": "Did you even test this before opening the PR?"},
            {"key": "C", "text": "Great work on the overall approach. I noticed that under concurrent transactions, this locking sequence might risk deadlocks. What do you think about adopting an optimistic lock pattern here?"},
            {"key": "D", "text": "I reject this pull request."},
        ],
        "correct_answer": "C",
        "explanation": "Option C acknowledges their effort, identifies the technical risk factually, and invites collaborative discussion with an alternative suggestion.",
        "category": "Professional Communication",
        "difficulty": "advanced",
        "level": 4,
    },

    # Level 5 - Executive Polish
    {
        "exercise_type": "professional_communication",
        "prompt": "Deliver a concise 2-sentence executive summary explaining why your team is migrating to microservices.",
        "options": [
            {"key": "A", "text": "We are migrating to modular services to decouple our deployment pipelines, enabling independent feature releases with 40% faster time-to-market. This architecture also isolates faults, ensuring higher system availability during peak traffic."},
            {"key": "B", "text": "Microservices are cool and modern so we are doing them because our old monolith is very old and annoying to work with."},
            {"key": "C", "text": "Everyone uses microservices nowadays so our company should also use them to look good."},
            {"key": "D", "text": "We are changing code because developers wanted new technology."},
        ],
        "correct_answer": "A",
        "explanation": "Option A ties technical architectural choices directly to strategic business metrics (faster time-to-market, fault isolation, high availability).",
        "category": "Professional Communication",
        "difficulty": "advanced",
        "level": 5,
    },
]


def seed_communication_exercises():
    """Seed communication module exercises."""
    for item in COMMUNICATION_DATA:
        existing = CommunicationExercise.query.filter_by(prompt=item["prompt"]).first()
        if not existing:
            e = CommunicationExercise(
                exercise_type=item["exercise_type"],
                prompt=item["prompt"],
                options=item["options"],
                correct_answer=item["correct_answer"],
                explanation=item["explanation"],
                category=item["category"],
                difficulty=item["difficulty"],
                level=item["level"],
            )
            db.session.add(e)
    db.session.commit()
