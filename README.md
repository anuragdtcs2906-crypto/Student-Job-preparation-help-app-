# Student-Job-preparation-help-app-
## AI-Powered Personalized Speaking & Communication Coach

A production-ready, privacy-first, modular platform designed to help students and job seekers build speaking confidence, pronunciation knowledge, interview mastery, presentation skills, and professional workplace communication in a supportive and encouraging environment.

---

## ⚡ Quick Start: Run Locally (Localhost)

Run the full interactive application locally in two simple commands:

```bash
# 1. Install dependencies (if not already installed)
pip install -r requirements.txt

# 2. Run the application
python run.py
```

Once running, open your web browser:
- 🌐 **Interactive Web App**: [http://localhost:5000](http://localhost:5000) or [http://127.0.0.1:5000](http://127.0.0.1:5000)
- 🩺 **API Health Check**: [http://localhost:5000/health](http://localhost:5000/health)

*(The database and initial seed content are auto-initialized on first run)*

---

## 🌟 Philosophy

> **"You choose what you want to improve. We figure out how you should practice."**

The platform is designed to build confidence through personalized practice. It never uses punitive, judgmental, or shaming language. Metrics measure engagement and progress without arbitrary pressure or forced streak penalties.

---

## 📋 Key Architecture & MVP Scope (V1)

1. **V1 MVP Learning Scope**:
   - Focuses on foundational phonetics, easy-to-read pronunciation spelling (e.g., `AR-ki-tek-cher`), syllable segmentation, stress awareness, example sentences, and revision tracking.
   - *Note: In accordance with V1 MVP scope, speech recording, speech-to-text, microphone input, and voice analysis are not implemented in V1.*
2. **Anonymous & Privacy-First User Model**:
   - No PII (no name, phone number, email, address, or college name) is ever requested or stored.
   - Users are assigned a unique, cryptographically secure 8-character anonymous ID (e.g., `AX7K29P4`) that serves as their public identifier to resume sessions anytime.
3. **Independent Multi-Goal Leveling**:
   - Proficiency levels (1 to 5) belong to individual goals, not to the user globally.
   - A user can be **Level 1** in Pronunciation, **Level 4** in Interview Preparation, and **Level 2** in Presentation Skills simultaneously.
4. **Deterministic Level Calculation**:
   - Diagnostic and progression level assignments follow database-configured deterministic score thresholds (`LevelConfiguration`), ensuring explainability and consistency.
5. **AI-Powered Personalization & Supportive Feedback**:
   - Combines assessment diagnostic results, current goal level, user-configured daily quantity targets, difficult content history, and spaced revision items to generate personalized practice sets.
   - The AI feedback engine evaluates open-ended responses using structured JSON outputs with supportive, confidence-building coaching.

---

## 🛠 Technology Stack

- **Runtime & Language**: Python 3.10+ / 3.14+
- **Web Framework**: Flask 3.1+ with Blueprint modular routing
- **ORM & Database**: SQLAlchemy 2.0+ & Flask-SQLAlchemy (PostgreSQL / SQLite for local testing)
- **Authentication**: Flask-JWT-Extended (Token-based stateless auth keyed to Anonymous User IDs)
- **Data & Recommendation**: Pandas, NumPy, Scikit-learn
- **AI Integration**: Official OpenAI Python SDK (Structured JSON mode with built-in Mock Fallback for offline environments)
- **Validation**: Pydantic 2.x & Marshmallow
- **Testing**: Pytest, Pytest-Cov, Pytest-Mock (54 automated tests with 92%+ code coverage)

---

## 📁 Project Structure

```text
backend/
├── app/
│   ├── __init__.py               # Flask application factory, error handlers, and extension registration
│   ├── config.py                 # Development, Testing, and Production configuration classes
│   ├── extensions.py             # SQLAlchemy, JWTManager, CORS, and Migrate instances
│   │
│   ├── models/                   # Normalized SQLAlchemy database models
│   │   ├── __init__.py
│   │   ├── user.py               # User (anonymous_id), UserGoal, DailyTarget, ActivityHistory
│   │   ├── goal.py               # Goal, Level (1-5), LevelConfiguration
│   │   ├── assessment.py         # Assessment, AssessmentQuestion, AssessmentAttempt, AssessmentAnswer
│   │   ├── content.py            # PronunciationWord, InterviewQuestion, PresentationTask, CommunicationExercise, GDQuestion
│   │   ├── practice.py           # PracticeSession, PracticeAttempt, UserProgress, UserRecommendation
│   │   └── ai_feedback.py        # AIFeedback (structured supportive JSON feedback)
│   │
│   ├── schemas/                  # Pydantic validation schemas
│   │   ├── __init__.py
│   │   ├── auth_schemas.py       # Anonymous login & ID validation
│   │   ├── goal_schemas.py       # Goal selection & daily target updates
│   │   ├── assessment_schemas.py # Diagnostic & progression assessment submissions
│   │   ├── practice_schemas.py   # Practice session lifecycle & attempt payloads
│   │   └── ai_schemas.py         # Direct AI evaluation request & structured output models
│   │
│   ├── repositories/             # Clean Data Access Layer (DAL)
│   │   ├── __init__.py
│   │   ├── user_repository.py
│   │   ├── goal_repository.py
│   │   ├── assessment_repository.py
│   │   ├── content_repository.py
│   │   └── practice_repository.py
│   │
│   ├── services/                 # Core domain business logic
│   │   ├── __init__.py
│   │   ├── auth_service.py       # Anonymous user creation & authentication
│   │   ├── goal_service.py       # Multi-goal selection & goal metadata
│   │   ├── target_service.py     # Content quantity daily targets
│   │   ├── assessment_service.py # Deterministic scoring & level assignment
│   │   ├── practice_service.py   # Practice sessions, attempt tracking, and AI feedback
│   │   ├── level_service.py      # Level metadata & progression readiness checks
│   │   ├── progress_service.py   # Dashboard analytics, activity calendar, time tracking
│   │   └── content_service.py    # Queries for Pronunciation, Interview, Presentation, Clear English, GD
│   │
│   ├── ai/                       # AI Service Layer
│   │   ├── __init__.py
│   │   ├── client.py             # Modular OpenAI client wrapper with mock fallback
│   │   ├── prompts.py            # Supportive coaching prompts (zero shaming / zero judgment)
│   │   ├── feedback_engine.py    # Structured JSON feedback generator & validator
│   │   └── assessment_helper.py  # Qualitative analysis for diagnostic assessments
│   │
│   ├── recommendation/           # Personalization Engine
│   │   ├── __init__.py
│   │   ├── engine.py             # Blends level, history, difficulty, revision, and targets
│   │   └── strategies.py         # Content distribution strategies
│   │
│   ├── routes/                   # Modular REST API Blueprints
│   │   ├── __init__.py
│   │   ├── auth_routes.py        # /api/v1/auth
│   │   ├── goal_routes.py        # /api/v1/goals
│   │   ├── assessment_routes.py  # /api/v1/assessments
│   │   ├── practice_routes.py    # /api/v1/practice
│   │   ├── pronunciation_routes.py # /api/v1/pronunciation
│   │   ├── interview_routes.py   # /api/v1/interviews
│   │   ├── presentation_routes.py# /api/v1/presentations
│   │   ├── communication_routes.py# /api/v1/communication
│   │   ├── gd_routes.py          # /api/v1/gd
│   │   ├── progress_routes.py    # /api/v1/dashboard & /api/v1/progress
│   │   ├── recommendation_routes.py # /api/v1/recommendations
│   │   └── ai_routes.py          # /api/v1/ai
│   │
│   └── utils/                    # Shared utilities
│       ├── __init__.py
│       ├── anonymous_id.py       # Secure 8-character ID generator & validator
│       ├── response.py           # Standardized JSON response helpers
│       ├── exceptions.py         # Custom application exceptions
│       ├── error_handlers.py     # Global error handling middleware
│       └── logger.py             # Structured logging setup
│
├── seed/                         # Seed data & automated database population
│   ├── __init__.py
│   ├── goals_seed.py             # 5 Goals, 25 Levels, and 25 LevelConfigurations
│   ├── pronunciation_seed.py     # Pronunciation dataset across levels 1-5
│   ├── interview_seed.py         # Interview questions across categories & levels
│   ├── presentation_seed.py      # Presentation tasks across categories & levels
│   ├── communication_seed.py     # Clear English exercises across categories & levels
│   ├── gd_seed.py                # GD scenarios across categories & levels
│   ├── assessment_seed.py        # Diagnostic & Progression assessments + questions
│   └── seed_runner.py            # Master idempotent seed runner
│
├── tests/                        # Comprehensive test suite
│   ├── conftest.py               # Test application, database fixtures, and auth headers
│   ├── unit/                     # Unit tests for core algorithms & services
│   ├── integration/              # End-to-end integration workflows
│   └── api/                      # REST API endpoint tests
│
├── .env.example                  # Environment configuration template
├── requirements.txt              # Pinned Python package dependencies
├── run.py                        # Application entrypoint & auto-seeder
└── README.md
```

---

## 🚀 Quick Start Guide

### 1. Clone & Set Up Virtual Environment

```bash
# Navigate to the project directory
cd "pronountiation app"

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# macOS/Linux:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root based on `.env.example`:

```env
FLASK_APP=run.py
FLASK_ENV=development
HOST=127.0.0.1
PORT=5000
SECRET_KEY=your-secure-secret-key-12345
DEBUG=True

# Database: PostgreSQL or local SQLite fallback
DATABASE_URL=sqlite:///communication_coach.db
# For PostgreSQL:
# DATABASE_URL=postgresql://postgres:password@localhost:5432/communication_coach_db

# JWT Secret
JWT_SECRET_KEY=your-jwt-secret-key-12345
JWT_ACCESS_TOKEN_EXPIRES_DAYS=30

# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-4o-mini
AI_MOCK_FALLBACK=True

# CORS
CORS_ORIGINS=*
```

### 3. Seed Database & Run the Server

```bash
# Seed all goals, levels, assessment questions, and learning datasets
python seed/seed_runner.py

# Start the Flask development server
python run.py
```

Open your browser and navigate to:
- **Interactive Web App**: [http://localhost:5000](http://localhost:5000) or [http://127.0.0.1:5000](http://127.0.0.1:5000)
- **API Health Check**: [http://localhost:5000/health](http://localhost:5000/health)

---

## 🧪 Running the Test Suite

Run the full automated test suite with pytest:

```bash
# Run all unit, integration, and API tests
pytest -v

# Run with test coverage report
pytest --cov=app --cov-report=term-missing
```

---

## 📡 Complete REST API Overview

All API responses follow a standardized JSON schema:

**Success Response**:
```json
{
  "success": true,
  "data": { ... },
  "message": "Optional descriptive message",
  "meta": { ... }
}
```

**Error Response**:
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Detailed error description"
  }
}
```

### 1. Authentication & Anonymous Identity (`/api/v1/auth`)

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/auth/anonymous` | Create a new anonymous user account and obtain JWT token. | No |
| `POST` | `/api/v1/auth/login` | Log in / resume session using 8-character anonymous ID. | No |
| `GET` | `/api/v1/auth/me` | Retrieve authenticated user profile, active goals, and targets. | Yes (JWT) |

### 2. Goals & Level Configuration (`/api/v1/goals`)

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/goals` | List all 5 available goals with their 5 levels. | No |
| `GET` | `/api/v1/goals/<slug>` | Get metadata and level descriptions for a single goal. | No |
| `POST` | `/api/v1/goals/select` | Activate one or multiple goals for the user. | Yes (JWT) |
| `GET` | `/api/v1/goals/my-goals` | List all goals currently activated by the user. | Yes (JWT) |
| `GET` | `/api/v1/goals/<slug>/levels` | List the 5 proficiency levels for a specific goal. | No |
| `GET` | `/api/v1/goals/<slug>/levels/<level_number>` | Get details and mastery thresholds for a specific level. | No |
| `GET` | `/api/v1/goals/<slug>/progression-status` | Check if user is ready for the next level progression check. | Yes (JWT) |
| `PUT` | `/api/v1/goals/<slug>/targets` | Set or update daily practice quantity target (e.g. 10 words). | Yes (JWT) |

### 3. Assessments & Diagnostic Evaluation (`/api/v1/assessments`)

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/assessments/<slug>/diagnostic` | Get initial diagnostic assessment questions for a goal. | No |
| `GET` | `/api/v1/assessments/<slug>/progression/<level_number>` | Get level progression assessment questions. | No |
| `POST` | `/api/v1/assessments/<slug>/submit` | Submit answers, receive deterministic starting level, strengths, and initial recommendations. | Yes (JWT) |
| `GET` | `/api/v1/assessments/<slug>/history` | Get past assessment attempts and score history. | Yes (JWT) |

### 4. Practice Sessions & Attempt Tracking (`/api/v1/practice`)

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/practice/sessions/start` | Start a new practice session for a goal with target quantity. | Yes (JWT) |
| `POST` | `/api/v1/practice/attempts` | Record practice item attempt (time spent, revision flag, optional AI feedback). | Yes (JWT) |
| `POST` | `/api/v1/practice/sessions/<session_id>/complete` | Complete and close a practice session, recording duration. | Yes (JWT) |
| `GET` | `/api/v1/practice/sessions/active/<slug>` | Get the current active practice session for a goal. | Yes (JWT) |

### 5. Learning Modules Content Datasets

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/v1/pronunciation/words` | List pronunciation words (filters: `level`, `category`, `limit`, `offset`). |
| `GET` | `/api/v1/pronunciation/words/<id>` | Get single pronunciation word details. |
| `GET` | `/api/v1/interviews/questions` | List interview questions (filters: `level`, `category`, `limit`, `offset`). |
| `GET` | `/api/v1/interviews/questions/<id>` | Get single interview question details. |
| `GET` | `/api/v1/presentations/tasks` | List presentation tasks (filters: `level`, `category`, `limit`, `offset`). |
| `GET` | `/api/v1/presentations/tasks/<id>` | Get single presentation task details. |
| `GET` | `/api/v1/communication/exercises` | List Clear English exercises (filters: `level`, `category`, `type`). |
| `GET` | `/api/v1/communication/exercises/<id>` | Get single communication exercise details. |
| `GET` | `/api/v1/gd/questions` | List Group Discussion scenarios (filters: `level`, `category`). |
| `GET` | `/api/v1/gd/questions/<id>` | Get single Group Discussion scenario details. |

### 6. Personal Progress & Dashboards (`/api/v1/dashboard` & `/api/v1/progress`)

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/dashboard` | Overall dashboard summarizing all active goals, total practice time, and 14-day calendar. | Yes (JWT) |
| `GET` | `/api/v1/progress/<goal_slug>` | In-depth analytics, revision queue, 30-day activity trend, and recent recommendations for a goal. | Yes (JWT) |

### 7. Recommendations Engine (`/api/v1/recommendations`)

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/recommendations/<goal_slug>` | Get dynamically generated personalized practice items (new level content + difficult items + spaced revision). | Yes (JWT) |

### 8. AI Direct Evaluation (`/api/v1/ai`)

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/ai/evaluate` | Request structured AI coaching feedback for any open-ended response text. | Yes (JWT) |

---

## 🧠 Recommendation Engine Mechanics

The recommendation engine combines multiple signals to determine what a user should practice next:

```text
User Daily Target (e.g. 10 items)
+ Current Goal Level
+ Previous Performance (Low scores or challenging items)
+ Revision Queue (Items marked for spaced review)
       ↓
Dynamic Distribution:
- 50% New Level-Appropriate Items
- 30% Previously Challenging / Low-Score Items
- 20% Spaced Revision Items
       ↓
Personalized Practice Set with Explainable Reasons
```

---

## 🤖 Supportive AI Feedback Principles

The AI feedback engine enforces strict psychological safety guidelines:
- **Always Positive First**: Identifies concrete strengths in the user's communication before offering suggestions.
- **Actionable Frameworks**: Recommends proven structures (e.g., STAR method for interviews, 3-part hooks for presentations, diplomatic transition phrasing for group discussions).
- **Zero Shaming**: Strictly forbids negative or derogatory labels.
- **Structured Output**: AI responses are validated via Pydantic before persisting to ensure database consistency.

---

## 🔒 Security & Privacy

- **No Personal Data Collected**: Privacy by design.
- **SQL Injection Protected**: All queries use SQLAlchemy ORM parameter binding.
- **Stateless Authentication**: Signed JWT tokens with configurable expiration.
- **CORS Configured**: Secure cross-origin resource sharing.
- **Environment Driven Secrets**: Secrets and database credentials loaded strictly from environment variables.
>>>>>>> 88a193b (Initial commit: AI Speaking & Communication Coach application with 3-page flow, diagnostic assessments, and level unlocking)
