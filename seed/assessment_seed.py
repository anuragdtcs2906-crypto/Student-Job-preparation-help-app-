from app.extensions import db
from app.models.goal import Goal
from app.models.assessment import Assessment, AssessmentQuestion

DIAGNOSTIC_ASSESSMENTS_DATA = [
    # 1. Pronunciation Diagnostic Assessment
    {
        "goal_slug": "pronunciation",
        "title": "Pronunciation & Phonetics Diagnostic Assessment",
        "assessment_type": "initial",
        "description": "Discover your current pronunciation awareness, syllable breakdown skill, and phonetic interpretation.",
        "total_points": 100,
        "pass_percentage": 75.0,
        "questions": [
            {
                "question_text": "How many distinct spoken syllables are in the word 'comfortable'?",
                "question_type": "syllable_count",
                "options": [
                    {"key": "A", "text": "2 syllables ('comf-table')"},
                    {"key": "B", "text": "3 syllables ('KUMF-ter-bul')"},
                    {"key": "C", "text": "4 syllables ('com-for-ta-ble')"},
                    {"key": "D", "text": "5 syllables ('com-for-ta-bi-le')"},
                ],
                "correct_answer": "B",
                "category": "Syllable Awareness",
                "difficulty": "beginner",
                "points": 20,
                "display_order": 1,
                "explanation": "Natural English reduces the middle vowel, resulting in 3 spoken syllables: 'KUMF-ter-bul'.",
            },
            {
                "question_text": "Which syllable receives the primary stress in the word 'photograph' versus 'photography'?",
                "question_type": "stress_choice",
                "options": [
                    {"key": "A", "text": "PHO-to-graph (1st) and pho-TOG-ra-phy (2nd)"},
                    {"key": "B", "text": "pho-TO-graph (2nd) and PHO-to-graphy (1st)"},
                    {"key": "C", "text": "Both have stress on the 1st syllable"},
                    {"key": "D", "text": "Both have stress on the 3rd syllable"},
                ],
                "correct_answer": "A",
                "category": "Stress Awareness",
                "difficulty": "intermediate",
                "points": 20,
                "display_order": 2,
                "explanation": "Adding '-y' shifts the stress from the 1st syllable 'PHO-to-graph' to the 2nd syllable 'pho-TOG-ra-phy'.",
            },
            {
                "question_text": "What is the accurate easy-to-read pronunciation spelling for the technical word 'architecture'?",
                "question_type": "multiple_choice",
                "options": [
                    {"key": "A", "text": "ar-chi-TEK-ture"},
                    {"key": "B", "text": "AR-ki-tek-cher"},
                    {"key": "C", "text": "arch-IT-ek-ture"},
                    {"key": "D", "text": "AR-tchi-tek-cher"},
                ],
                "correct_answer": "B",
                "category": "Phonetic Breakdown",
                "difficulty": "intermediate",
                "points": 20,
                "display_order": 3,
                "explanation": "The 'ch' is pronounced as a hard 'k', making the easy spelling 'AR-ki-tek-cher'.",
            },
            {
                "question_text": "In the sentence 'I need to record a record for the podcast', which pronunciation pattern is correct for the verb and noun pair?",
                "question_type": "multiple_choice",
                "options": [
                    {"key": "A", "text": "Verb: RE-cord / Noun: re-CORD"},
                    {"key": "B", "text": "Verb: rih-CORD / Noun: REK-erd"},
                    {"key": "C", "text": "Both are pronounced REK-erd"},
                    {"key": "D", "text": "Both are pronounced rih-CORD"},
                ],
                "correct_answer": "B",
                "category": "Word Class Stress Shifts",
                "difficulty": "intermediate",
                "points": 20,
                "display_order": 4,
                "explanation": "English two-syllable noun/verb pairs typically stress the 2nd syllable for verbs ('rih-CORD') and the 1st for nouns ('REK-erd').",
            },
            {
                "question_text": "What is the primary stress and syllable breakdown of 'methodology'?",
                "question_type": "multiple_choice",
                "options": [
                    {"key": "A", "text": "METH-uh-dol-uh-jee (1st syllable)"},
                    {"key": "B", "text": "meth-UH-dol-uh-jee (2nd syllable)"},
                    {"key": "C", "text": "meth-uh-DOL-uh-jee (3rd syllable)"},
                    {"key": "D", "text": "meth-uh-dol-UH-jee (4th syllable)"},
                ],
                "correct_answer": "C",
                "category": "Multi-Syllabic Words",
                "difficulty": "advanced",
                "points": 20,
                "display_order": 5,
                "explanation": "Words ending in '-ology' consistently place primary stress on the syllable preceding 'ology': 'meth-uh-DOL-uh-jee'.",
            },
        ],
    },

    # 2. Interview Diagnostic Assessment
    {
        "goal_slug": "interview",
        "title": "Interview Readiness Diagnostic Assessment",
        "assessment_type": "initial",
        "description": "Assess your understanding of interview response frameworks, behavioral answers, and structured communication.",
        "total_points": 100,
        "pass_percentage": 75.0,
        "questions": [
            {
                "question_text": "When an interviewer asks 'Tell me about yourself', what is the most effective structure to follow?",
                "question_type": "multiple_choice",
                "options": [
                    {"key": "A", "text": "Start from childhood, recount all high school grades, and list all courses taken."},
                    {"key": "B", "text": "Present (current role/skills) -> Past (key relevant accomplishments) -> Future (why you fit this role)."},
                    {"key": "C", "text": "Ask the interviewer to read your resume aloud so you can confirm details."},
                    {"key": "D", "text": "List only personal hobbies without mentioning professional experience."},
                ],
                "correct_answer": "B",
                "category": "Introduction Strategy",
                "difficulty": "beginner",
                "points": 20,
                "display_order": 1,
                "explanation": "The Present-Past-Future model is concise, structured, and immediately positions your relevance.",
            },
            {
                "question_text": "What does the STAR framework stand for in behavioral interview responses?",
                "question_type": "multiple_choice",
                "options": [
                    {"key": "A", "text": "Strategy, Tactics, Assessment, Review"},
                    {"key": "B", "text": "Situation, Task, Action, Result"},
                    {"key": "C", "text": "Strength, Talent, Ambition, Responsibility"},
                    {"key": "D", "text": "Speed, Teamwork, Agility, Resilience"},
                ],
                "correct_answer": "B",
                "category": "STAR Framework",
                "difficulty": "beginner",
                "points": 20,
                "display_order": 2,
                "explanation": "STAR (Situation, Task, Action, Result) ensures complete, evidence-based storytelling.",
            },
            {
                "question_text": "Which component of the STAR method should receive the most time and detail in your answer?",
                "question_type": "multiple_choice",
                "options": [
                    {"key": "A", "text": "Situation (spending 80% on background history)"},
                    {"key": "B", "text": "Task (describing what other people should have done)"},
                    {"key": "C", "text": "Action (what YOU specifically did, your thought process, and leadership)"},
                    {"key": "D", "text": "All sections must be strictly identical in word count"},
                ],
                "correct_answer": "C",
                "category": "STAR Framework",
                "difficulty": "intermediate",
                "points": 20,
                "display_order": 3,
                "explanation": "Interviewers evaluate your personal contribution, problem-solving, and specific actions.",
            },
            {
                "question_text": "How should you frame a 'weakness' or area of improvement when asked by an interviewer?",
                "question_type": "multiple_choice",
                "options": [
                    {"key": "A", "text": "Say 'I have no weaknesses' to project supreme confidence."},
                    {"key": "B", "text": "Mention a real skill, explain how you became aware of it, and highlight concrete steps you are actively taking to improve."},
                    {"key": "C", "text": "Use a cliché disguise like 'I work too hard and care too much'."},
                    {"key": "D", "text": "List severe interpersonal issues without any resolution."},
                ],
                "correct_answer": "B",
                "category": "Constructive Growth",
                "difficulty": "intermediate",
                "points": 20,
                "display_order": 4,
                "explanation": "Genuine self-awareness coupled with active growth demonstrates emotional maturity and coachability.",
            },
            {
                "question_text": "At the end of an interview, the interviewer asks: 'Do you have any questions for us?' What is the best approach?",
                "question_type": "multiple_choice",
                "options": [
                    {"key": "A", "text": "Say 'No, you covered everything' and end the call immediately."},
                    {"key": "B", "text": "Ask 1-2 thoughtful questions about team engineering culture, upcoming challenges, or day-to-day collaboration."},
                    {"key": "C", "text": "Ask immediately about exact vacation days and holiday policy."},
                    {"key": "D", "text": "Ask the interviewer personal salary details."},
                ],
                "correct_answer": "B",
                "category": "Closing & Engagement",
                "difficulty": "intermediate",
                "points": 20,
                "display_order": 5,
                "explanation": "Asking thoughtful questions demonstrates curiosity, engagement, and long-term interest.",
            },
        ],
    },

    # 3. Presentation Diagnostic Assessment
    {
        "goal_slug": "presentation",
        "title": "Presentation Skills Diagnostic Assessment",
        "assessment_type": "initial",
        "description": "Evaluate your understanding of presentation organization, audience hooks, slide clarity, and Q&A composure.",
        "total_points": 100,
        "pass_percentage": 75.0,
        "questions": [
            {
                "question_text": "What is the most effective way to begin a presentation to capture immediate audience attention?",
                "question_type": "multiple_choice",
                "options": [
                    {"key": "A", "text": "Read the entire table of contents slide bullet by bullet in a monotone voice."},
                    {"key": "B", "text": "Start with an engaging hook: a compelling question, surprising statistic, or brief relatable problem story."},
                    {"key": "C", "text": "Apologize in advance for being unprepared or nervous."},
                    {"key": "D", "text": "Jump into code lines without explaining what the system does."},
                ],
                "correct_answer": "B",
                "category": "Opening Hooks",
                "difficulty": "beginner",
                "points": 20,
                "display_order": 1,
                "explanation": "An engaging hook builds immediate audience curiosity and connection.",
            },
            {
                "question_text": "What is the ideal guideline for text density on presentation slides?",
                "question_type": "multiple_choice",
                "options": [
                    {"key": "A", "text": "Paste full paragraphs so the audience can read while you speak."},
                    {"key": "B", "text": "Keep slides clean with concise bullet points or visuals that support your spoken narrative."},
                    {"key": "C", "text": "Use as many different bright font colors as possible on every slide."},
                    {"key": "D", "text": "Never include any text or visuals at all."},
                ],
                "correct_answer": "B",
                "category": "Slide Design & Clarity",
                "difficulty": "beginner",
                "points": 20,
                "display_order": 2,
                "explanation": "Slides should complement your speech, not compete with it through dense walls of text.",
            },
            {
                "question_text": "When presenting a complex technical concept to a cross-functional audience, what technique works best?",
                "question_type": "multiple_choice",
                "options": [
                    {"key": "A", "text": "Use specialized acronyms without defining them."},
                    {"key": "B", "text": "Use everyday analogies and connect technical choices to user or business outcomes."},
                    {"key": "C", "text": "Skip explanations and tell the audience to look it up later."},
                    {"key": "D", "text": "Speak faster so you can cover more complex equations."},
                ],
                "correct_answer": "B",
                "category": "Technical Explanations",
                "difficulty": "intermediate",
                "points": 20,
                "display_order": 3,
                "explanation": "Analogies bridge the gap between technical mechanics and human understanding.",
            },
            {
                "question_text": "If an audience member asks a question during Q&A that you do not know the exact answer to, what should you do?",
                "question_type": "multiple_choice",
                "options": [
                    {"key": "A", "text": "Make up an answer on the spot hoping nobody notices."},
                    {"key": "B", "text": "Acknowledge the insightful question, share your current understanding, and commit to following up with the verified answer."},
                    {"key": "C", "text": "Ignore the question and pretend you didn't hear it."},
                    {"key": "D", "text": "Tell them the question is irrelevant."},
                ],
                "correct_answer": "B",
                "category": "Q&A Handling",
                "difficulty": "intermediate",
                "points": 20,
                "display_order": 4,
                "explanation": "Composed honesty builds credibility and trust with professional audiences.",
            },
            {
                "question_text": "What makes a strong, memorable conclusion to a presentation?",
                "question_type": "multiple_choice",
                "options": [
                    {"key": "A", "text": "Saying 'Yeah, that's pretty much all I have' and trailing off."},
                    {"key": "B", "text": "A concise recap of the 2-3 key takeaways and a clear, inspiring call to action."},
                    {"key": "C", "text": "Introducing 5 brand new topics in the final 30 seconds."},
                    {"key": "D", "text": "Abruptly switching to a blank screen."},
                ],
                "correct_answer": "B",
                "category": "Conclusions & Impact",
                "difficulty": "intermediate",
                "points": 20,
                "display_order": 5,
                "explanation": "A structured conclusion reinforces main takeaways and leaves a lasting positive impression.",
            },
        ],
    },

    # 4. Clear English Diagnostic Assessment
    {
        "goal_slug": "communication",
        "title": "Clear English & Workplace Communication Diagnostic",
        "assessment_type": "initial",
        "description": "Assess your sentence structure, conciseness, active voice, and professional communication nuance.",
        "total_points": 100,
        "pass_percentage": 75.0,
        "questions": [
            {
                "question_text": "Which sentence is the most concise and direct?",
                "question_type": "sentence_choice",
                "options": [
                    {"key": "A", "text": "In spite of the fact that we were experiencing technical difficulties, we were able to complete the deployment."},
                    {"key": "B", "text": "Although we faced technical difficulties, we completed the deployment."},
                    {"key": "C", "text": "Technical difficulties were experienced by our team notwithstanding we completed deploying."},
                    {"key": "D", "text": "We did the deployment completion due to having difficulties notwithstanding."},
                ],
                "correct_answer": "B",
                "category": "Conciseness",
                "difficulty": "beginner",
                "points": 20,
                "display_order": 1,
                "explanation": "Option B eliminates unnecessary filler words while maintaining complete clarity.",
            },
            {
                "question_text": "Which sentence uses the active voice effectively?",
                "question_type": "sentence_choice",
                "options": [
                    {"key": "A", "text": "The database was optimized by our backend team to reduce latency."},
                    {"key": "B", "text": "Our backend team optimized the database to reduce latency."},
                    {"key": "C", "text": "Optimization of the database was performed by backend engineers."},
                    {"key": "D", "text": "Latency was reduced through database optimization being done by the team."},
                ],
                "correct_answer": "B",
                "category": "Active Voice",
                "difficulty": "beginner",
                "points": 20,
                "display_order": 2,
                "explanation": "Active voice puts the actor ('Our backend team') before the verb ('optimized').",
            },
            {
                "question_text": "You need to decline an invitation to an optional meeting due to an urgent sprint deadline. What is the most professional response?",
                "question_type": "multiple_choice",
                "options": [
                    {"key": "A", "text": "I can't come, I'm too busy with real work."},
                    {"key": "B", "text": "Thank you for the invite. Due to an urgent sprint deadline today, I won't be able to attend live, but I will review the meeting notes and send my input asynchronously."},
                    {"key": "C", "text": "No."},
                    {"key": "D", "text": "Why did you invite me to this?"},
                ],
                "correct_answer": "B",
                "category": "Professional Courtesy",
                "difficulty": "intermediate",
                "points": 20,
                "display_order": 3,
                "explanation": "Option B is polite, transparent about constraints, and offers proactive asynchronous collaboration.",
            },
            {
                "question_text": "Which word best completes the professional sentence: 'The team conducted a comprehensive audit to [____] potential bottlenecks in the pipeline.'",
                "question_type": "multiple_choice",
                "options": [
                    {"key": "A", "text": "spot out"},
                    {"key": "B", "text": "identify"},
                    {"key": "C", "text": "catch up on"},
                    {"key": "D", "text": "look-see"},
                ],
                "correct_answer": "B",
                "category": "Professional Vocabulary",
                "difficulty": "intermediate",
                "points": 20,
                "display_order": 4,
                "explanation": "'Identify' is the precise professional term for recognizing and pinpointing system bottlenecks.",
            },
            {
                "question_text": "Which sentence avoids unnecessary jargon while remaining technically accurate?",
                "question_type": "sentence_choice",
                "options": [
                    {"key": "A", "text": "We need to synergize our core competencies to leverage paradigm-shifting cloud solutions."},
                    {"key": "B", "text": "We are migrating our services to the cloud to increase uptime and lower server costs."},
                    {"key": "C", "text": "Our cross-pollination of ideation frameworks will disrupt the ecosystem."},
                    {"key": "D", "text": "Cloudification enablement will maximize our bandwidth throughput matrix."},
                ],
                "correct_answer": "B",
                "category": "Clarity & Simplicity",
                "difficulty": "intermediate",
                "points": 20,
                "display_order": 5,
                "explanation": "Option B conveys tangible business value in plain, clear, professional language.",
            },
        ],
    },

    # 5. GD & Professional Communication Diagnostic Assessment
    {
        "goal_slug": "gd",
        "title": "Group Discussion & Professional Communication Diagnostic",
        "assessment_type": "initial",
        "description": "Assess your ability to initiate discussion points, disagree respectfully, build consensus, and summarize collaborative meetings.",
        "total_points": 100,
        "pass_percentage": 75.0,
        "questions": [
            {
                "question_text": "What is the most constructive way to enter an ongoing group discussion without interrupting rudely?",
                "question_type": "multiple_choice",
                "options": [
                    {"key": "A", "text": "Start shouting over the current speaker until they stop talking."},
                    {"key": "B", "text": "Wait for a natural pause, then say: 'Building on what Maya just mentioned, I'd like to add another perspective...'"},
                    {"key": "C", "text": "Wave your hands aggressively and say 'Listen to me now'."},
                    {"key": "D", "text": "Stay silent the entire time and don't participate at all."},
                ],
                "correct_answer": "B",
                "category": "Entering Discussions",
                "difficulty": "beginner",
                "points": 20,
                "display_order": 1,
                "explanation": "Referencing the previous speaker connects your contribution seamlessly to the group conversation.",
            },
            {
                "question_text": "A team member proposes an idea you believe has serious budget risks. How do you express your disagreement respectfully?",
                "question_type": "multiple_choice",
                "options": [
                    {"key": "A", "text": "Say 'That is a terrible idea and will waste all our money.'"},
                    {"key": "B", "text": "Say 'I appreciate the creative direction of this proposal. One factor we should consider carefully is the budget allocation; perhaps we could pilot a smaller version first?'"},
                    {"key": "C", "text": "Roll your eyes and laugh."},
                    {"key": "D", "text": "Tell them they don't understand finances."},
                ],
                "correct_answer": "B",
                "category": "Respectful Disagreement",
                "difficulty": "intermediate",
                "points": 20,
                "display_order": 2,
                "explanation": "Validating the intent before offering risk analysis and constructive alternatives fosters safe collaboration.",
            },
            {
                "question_text": "In a Group Discussion, what is the role of an effective participant when two members are in a deadlock?",
                "question_type": "multiple_choice",
                "options": [
                    {"key": "A", "text": "Take one side aggressively and attack the other person."},
                    {"key": "B", "text": "Step in neutrally: 'It seems both points highlight critical priorities—quality and speed. Let's see how we can combine them into a phased approach.'"},
                    {"key": "C", "text": "Let them argue forever while staying silent."},
                    {"key": "D", "text": "Leave the room."},
                ],
                "correct_answer": "B",
                "category": "Consensus Building",
                "difficulty": "intermediate",
                "points": 20,
                "display_order": 3,
                "explanation": "Synthesizing opposing views into shared solutions is a hallmark of leadership in group discussions.",
            },
            {
                "question_text": "Which phrase is best for asking a speaker to clarify an ambiguous point in a meeting?",
                "question_type": "multiple_choice",
                "options": [
                    {"key": "A", "text": "Your point made zero sense. Explain it better."},
                    {"key": "B", "text": "Could you help me understand how this solution will handle offline data sync?"},
                    {"key": "C", "text": "Why are you being so vague?"},
                    {"key": "D", "text": "Whatever you said was confusing."},
                ],
                "correct_answer": "B",
                "category": "Clarifying Questions",
                "difficulty": "intermediate",
                "points": 20,
                "display_order": 4,
                "explanation": "Asking targeted, curious questions encourages depth without creating defensiveness.",
            },
            {
                "question_text": "How should a group discussion summary be delivered at the conclusion of a session?",
                "question_type": "multiple_choice",
                "options": [
                    {"key": "A", "text": "Only repeat your own personal opinions and declare yourself the winner."},
                    {"key": "B", "text": "Deliver a balanced summary highlighting key viewpoints discussed and the group's collective consensus."},
                    {"key": "C", "text": "List who spoke the most versus least words."},
                    {"key": "D", "text": "Say 'We talked about many things' and stop."},
                ],
                "correct_answer": "B",
                "category": "Summarization",
                "difficulty": "intermediate",
                "points": 20,
                "display_order": 5,
                "explanation": "An effective summary represents the entire group's contributions fairly and neutrally.",
            },
        ],
    },
]


def seed_assessments():
    """Seed diagnostic assessments and questions for all 5 goals."""
    for a_data in DIAGNOSTIC_ASSESSMENTS_DATA:
        goal = Goal.query.filter_by(slug=a_data["goal_slug"]).first()
        if not goal:
            continue

        assessment = Assessment.query.filter_by(
            goal_id=goal.id, assessment_type=a_data["assessment_type"], level_number=None
        ).first()

        if not assessment:
            assessment = Assessment(
                goal_id=goal.id,
                level_number=None,
                title=a_data["title"],
                assessment_type=a_data["assessment_type"],
                description=a_data["description"],
                total_points=a_data["total_points"],
                pass_percentage=a_data["pass_percentage"],
            )
            db.session.add(assessment)
            db.session.flush()

        for q_data in a_data["questions"]:
            existing_q = AssessmentQuestion.query.filter_by(
                assessment_id=assessment.id, question_text=q_data["question_text"]
            ).first()

            if not existing_q:
                q = AssessmentQuestion(
                    assessment_id=assessment.id,
                    goal_id=goal.id,
                    level_number=None,
                    assessment_type=a_data["assessment_type"],
                    question_text=q_data["question_text"],
                    question_type=q_data["question_type"],
                    options=q_data["options"],
                    correct_answer=q_data["correct_answer"],
                    category=q_data["category"],
                    difficulty=q_data["difficulty"],
                    points=q_data["points"],
                    display_order=q_data["display_order"],
                    explanation=q_data["explanation"],
                )
                db.session.add(q)

        # Also seed Level Progression Assessments (Levels 1-4) for each goal
        for lvl_num in range(1, 5):
            prog_assessment = Assessment.query.filter_by(
                goal_id=goal.id, assessment_type="level_progression", level_number=lvl_num
            ).first()

            if not prog_assessment:
                prog_assessment = Assessment(
                    goal_id=goal.id,
                    level_number=lvl_num,
                    title=f"{goal.name} - Level {lvl_num} Progression Check",
                    assessment_type="level_progression",
                    description=f"Demonstrate mastery of Level {lvl_num} skills to advance to Level {lvl_num + 1}.",
                    total_points=100,
                    pass_percentage=75.0,
                )
                db.session.add(prog_assessment)
                db.session.flush()

                # Add 4 sample progression questions for each level
                for q_idx in range(1, 5):
                    prog_q = AssessmentQuestion(
                        assessment_id=prog_assessment.id,
                        goal_id=goal.id,
                        level_number=lvl_num,
                        assessment_type="level_progression",
                        question_text=f"Level {lvl_num} Mastery Check Question {q_idx} for {goal.name}",
                        question_type="multiple_choice",
                        options=[
                            {"key": "A", "text": "Mastery approach with structured application"},
                            {"key": "B", "text": "Incomplete approach"},
                            {"key": "C", "text": "Unstructured alternative"},
                            {"key": "D", "text": "Passive alternative"},
                        ],
                        correct_answer="A",
                        category=f"Level {lvl_num} Mastery",
                        difficulty="intermediate",
                        points=25,
                        display_order=q_idx,
                        explanation=f"Option A demonstrates clear Level {lvl_num} proficiency.",
                    )
                    db.session.add(prog_q)

    db.session.commit()
