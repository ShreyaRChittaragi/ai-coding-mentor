# 🧠 AI Coding Mentor

---

## 🚀 Live Demo

| Service | URL |
|---|---|
| 🖥️ Frontend | https://ai-coding-mentor-chi.vercel.app/ |
| ⚙️ Backend API | https://ai-coding-mentor-backend.onrender.com |
| 📖 API Docs (Swagger) | https://ai-coding-mentor-backend.onrender.com/docs |

---

## 📌 What Is This?

AI Coding Mentor is a system where students submit Python solutions to coding problems and receive **personalized, memory-driven hints** — not generic feedback.

The system doesn't ask users how they learn. It **watches how they actually behave**:
- How fast they submit
- How many times they edit their code
- What kinds of errors they make
- How many attempts they take

It converts these behavioral signals into **cognitive pattern labels** — then uses [Hindsight](https://hindsight.vectorize.io/) to persist that knowledge across sessions. Every hint, every next problem, every encouragement message is adapted to what the system knows about that specific user.

---

## 🧠 How Hindsight Memory Works

This is the core of the system. Every code submission triggers a full memory pipeline:

```
User submits code
        ↓
execution_service.py   — runs code against test cases
        ↓
signal_tracker.py      — captures time_taken, edit_count, error_types, attempts
        ↓
cognitive_analyzer.py  — converts signals into pattern labels + confidence scores
        ↓
hindsight.py           — stores patterns to Hindsight Cloud via retain()
        ↓
On next session:
  recall()             — retrieves user's behavioral profile
  reflect()            — generates adaptive LLM instructions
        ↓
Groq LLM               — produces hint tailored to THIS user's patterns
```

### Cognitive Patterns Detected

| Pattern | Signal | Response |
|---|---|---|
| `rushing` | Fast submit + syntax errors + few edits | Slow down, re-read the problem |
| `overthinking` | Long time + few attempts + eventually passes | Trust your instinct, start simple |
| `guessing` | Many attempts + very short time + all fail | Think step by step before submitting |
| `concept_gap` | Specific error types (NameError, TypeError) | Back to basics |
| `boundary_weakness` | Passes most cases, fails edge cases | Think about boundary conditions |

### Hindsight Integration Code

```python
# Store a session into Hindsight Cloud
def store_session(user_id: str, session_data: dict):
    _run_in_new_loop(client.aretain(
        bank_id="coding-mentor",
        content=f"User {user_id} showed {session_data['dominant_pattern']} pattern...",
        context=f"coding session for user {user_id}",
        metadata={"user_id": user_id}
    ))

# Reflect on user history to generate adaptive LLM instructions
def reflect_on_user(user_id: str, question: str) -> str:
    answer = _run_in_new_loop(client.areflect(
        bank_id="coding-mentor",
        query=question,
        budget="low",
        context=f"This question is about user {user_id}"
    ))
    return answer.text
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        FRONTEND                             │
│              React + Monaco Editor (Vercel)                 │
│   Code Editor │ Feedback Panel │ Insights │ Next Problem    │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP
┌──────────────────────────▼──────────────────────────────────┐
│                      FASTAPI BACKEND                        │
│                      (Render)                               │
│                                                             │
│  /submit_code    /get_feedback    /get_problem              │
│  /user_profile   /next_problem    /memory/*                 │
└────┬─────────────────┬───────────────────┬──────────────────┘
     │                 │                   │
┌────▼────┐    ┌───────▼──────┐   ┌────────▼────────┐
│Execution│    │  Groq LLM    │   │    Hindsight     │
│ Engine  │    │ LLaMA 3.3 70B│   │  Cloud Memory    │
│         │    │              │   │                  │
│run_user │    │ prompt_      │   │ retain()         │
│_code()  │    │ builder.py   │   │ recall()         │
│         │    │ feedback_    │   │ reflect()        │
│signal_  │    │ service.py   │   │                  │
│tracker  │    │              │   │ Behavioral       │
│         │    │ Adaptive     │   │ profiles stored  │
│cognitive│    │ hints based  │   │ across sessions  │
│_analyzer│    │ on memory    │   │                  │
└─────────┘    └──────────────┘   └──────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI (Python 3.13) |
| LLM | Groq — LLaMA 3.3 70B Versatile |
| Memory | Hindsight Cloud |
| Frontend | React + Vite + Monaco Editor |
| Code Execution | Python `exec()` + threading timeout |
| Deployment | Render (backend) + Vercel (frontend) |

---

## ⚙️ Local Setup

### Prerequisites
- Python 3.13+
- Node.js 18+
- Git

### 1. Clone the repository

```bash
git clone https://github.com/ShreyaRChittaragi/ai-coding-mentor.git
cd ai-coding-mentor
```

### 2. Set up the backend

```bash
# Create and activate virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and add your keys:

```
GROQ_API_KEY=your_groq_key_here
HINDSIGHT_API_KEY=your_hindsight_key_here
HINDSIGHT_URL=https://api.hindsight.vectorize.io
DEBUG=True
```

Get your keys:
- Groq → https://console.groq.com
- Hindsight → https://ui.hindsight.vectorize.io

### 4. Run the backend

```bash
uvicorn app.main:app --reload
```

Backend runs at → `http://127.0.0.1:8000`
Swagger docs → `http://127.0.0.1:8000/docs`

### 5. Run the frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at → `http://localhost:5173`

---

## 📡 API Endpoints

### Problems
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/get_problem/{problem_id}` | Get a problem by ID (e.g. p001) |
| `GET` | `/problems` | List all 9 problems |
| `GET` | `/problems/difficulty/{difficulty}` | Filter by easy / medium / hard |
| `GET` | `/problems/topic/{topic}` | Filter by topic (arrays, strings, etc.) |

### Code Execution
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/submit_code` | Submit code, run tests, detect patterns, store memory |

```json
// POST /submit_code — example request
{
  "user_id": "user_001",
  "problem_id": "p001",
  "code": "def two_sum(nums, target):\n    pass",
  "language": "python",
  "time_taken": 45.0,
  "attempt_number": 1,
  "code_edit_count": 5
}
```

### Feedback
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/get_feedback` | Get Groq LLM hint adapted to user memory |

### Memory
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/memory/recall/{user_id}` | Get full Hindsight memory profile |
| `POST` | `/memory/store` | Manually store a session |
| `POST` | `/memory/adaptive-prompt` | Build memory-aware LLM prompt |
| `GET` | `/memory/adaptive-context/{user_id}/{topic}` | Get adaptive context for a topic |

### User & Adaptive
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/user_profile/{user_id}` | Get user profile with weak areas |
| `GET` | `/next_problem/{user_id}` | Get adaptive next problem recommendation |
| `GET` | `/user_pattern/{user_id}` | Get dominant behavioral pattern |
| `GET` | `/visualizations/{user_id}` | Get chart data for frontend |

### Health
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Root health check |
| `GET` | `/health` | Server health check |

---

## 🧪 Running Tests

```bash
python -m pytest tests/test_routes.py -v
```

Expected output:
```
tests/test_routes.py::test_root                PASSED
tests/test_routes.py::test_health              PASSED
tests/test_routes.py::test_get_problem         PASSED
tests/test_routes.py::test_get_all_problems    PASSED
tests/test_routes.py::test_submit_code         PASSED
tests/test_routes.py::test_get_feedback        PASSED
tests/test_routes.py::test_user_profile        PASSED
tests/test_routes.py::test_visualizations      PASSED

8 passed
```

---

## 👥 Team — 1/0 Coders

| # | Name | Role | Article |
|---|---|---|---|
| 1 | Shreya R Chittaragi | Memory & Adaptation | [Read Article][article1] |
| 2 | Devika N D | Code Execution & Behavioral Signals | [Read Article][article2] |
| 3 | Chiranjeevi C | React Frontend | [Read Article][article3] |
| 4 | Kiran H | QA, Documentation & GitHub | [Read Article][article4] |
| 5 | Jagadeesh R S | API Layer & Models | [Read Article][article5] |

[article1]: [post link]
[article2]: [post link]
[article3]: [post link]
[article4]: [post link]
[article5]: [post link]

---

## 📁 Project Structure

```
ai-coding-mentor/
├── app/
│   ├── main.py                    ← FastAPI entry point
│   ├── api/
│   │   └── routes/
│   │       ├── memory.py          ← Memory routes
│   │       ├── submit_code.py     ← Code execution route
│   │       ├── get_problem.py     ← Problem routes
│   │       ├── get_feedback.py    ← LLM feedback route
│   │       ├── user_profile.py    ← User profile route
│   │       ├── next_problem.py    ← Adaptive selector route
│   │       └── visualizations.py ← Chart data route
│   ├── core/
│   │   └── config.py             ← Environment settings
│   ├── memory/
│   │   ├── hindsight.py          ← Hindsight Cloud integration
│   │   ├── schemas.py            ← Memory data models
│   │   ├── patterns.py           ← Pattern detection wrapper
│   │   └── adaptive_selector.py  ← Next problem logic
│   ├── models/
│   │   └── __init__.py           ← Shared Pydantic models
│   └── services/
│       ├── execution_service.py  ← Code runner + timeout
│       ├── signal_tracker.py     ← Behavioral signal capture
│       ├── cognitive_analyzer.py ← Pattern detection engine
│       ├── feedback_service.py   ← LLM feedback orchestration
│       ├── groq_client.py        ← Groq API client
│       ├── prompt_builder.py     ← Adaptive prompt builder
│       ├── problem_store.py      ← Problem loader
│       └── problem_generator.py  ← AI problem generator
├── frontend/
│   └── src/
│       ├── App.jsx
│       └── components/
│           ├── CodeEditor.jsx
│           ├── FeedbackPanel.jsx
│           ├── InsightsPanel.jsx
│           ├── PatternChart.jsx
│           ├── ProblemPanel.jsx
│           └── FilterBar.jsx
├── tests/
│   └── test_routes.py
├── .env.example
├── requirements.txt
└── README.md
```

---

## 🔗 Resources

- [Hindsight Documentation](https://hindsight.vectorize.io/)
- [Hindsight GitHub](https://github.com/vectorize-io/hindsight)
- [Agent Memory — Vectorize](https://vectorize.io/features/agent-memory)
- [Groq Console](https://console.groq.com)
- [FastAPI Docs](https://fastapi.tiangolo.com/)

---

*Built at HackWithIndia by Team 1/0 Coders*
